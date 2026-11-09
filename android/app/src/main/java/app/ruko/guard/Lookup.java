package app.ruko.guard;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;

/** Looks up a number in Ruko's community reports (Supabase RPC number_lookup). */
final class Lookup {
    static final String SITE = "https://ruko-ohn2.onrender.com";
    static final String SUPABASE_URL = "https://izxqlbipvrtnsvpwekaw.supabase.co";
    // Publishable key: public by design (same as web/config.js); row-level security protects the data.
    static final String SUPABASE_KEY = "sb_publishable_M8we6sPJuWsmIZOZuKQbrQ_pivd7C1I";
    /** Same rule as the website: one report alone never marks a number. */
    static final int MIN_REPORTS = 2;

    static final class Result {
        final int reports;
        final String category;
        Result(int reports, String category) { this.reports = reports; this.category = category; }
        boolean flagged() { return reports >= MIN_REPORTS; }
    }

    /** "+91 98765-43210" or "098765 43210" -> "9876543210"; other numbers keep all their digits. */
    static String normalize(String raw) {
        if (raw == null) return "";
        String d = raw.replaceAll("\\D", "");
        if (d.length() >= 10 && "6789".indexOf(d.charAt(d.length() - 10)) >= 0) return d.substring(d.length() - 10);
        return d;
    }

    static String label(String category) {
        if (category == null) return "a scam";
        switch (category) {
            case "digital_arrest": return "fake police / CBI";
            case "bank_kyc": return "a bank or KYC scam";
            case "electricity": return "an electricity cut-off scam";
            case "parcel": return "a parcel or customs scam";
            case "refund": return "a “sent by mistake” scam";
            case "relative": return "a relative-in-trouble scam";
            case "job": return "a job or task scam";
            case "prize": return "a prize or lottery scam";
            case "loan": return "a loan scam";
            default: return "a scam";
        }
    }

    static Result parse(String json) throws Exception {
        JSONArray a = new JSONArray(json);
        if (a.length() == 0) return new Result(0, null);
        JSONObject o = a.getJSONObject(0);
        return new Result(o.optInt("reports", 0), o.isNull("top_category") ? null : o.optString("top_category", null));
    }

    /** Blocking network call; never run it on the main thread. */
    static Result fetch(String number) throws Exception {
        HttpURLConnection c = (HttpURLConnection) new URL(SUPABASE_URL + "/rest/v1/rpc/number_lookup").openConnection();
        c.setConnectTimeout(3000);
        c.setReadTimeout(3000);
        c.setRequestMethod("POST");
        c.setDoOutput(true);
        c.setRequestProperty("apikey", SUPABASE_KEY);
        c.setRequestProperty("Authorization", "Bearer " + SUPABASE_KEY);
        c.setRequestProperty("Content-Type", "application/json");
        try (OutputStream os = c.getOutputStream()) {
            os.write(new JSONObject().put("p_number", number).toString().getBytes(StandardCharsets.UTF_8));
        }
        if (c.getResponseCode() != 200) throw new Exception("lookup " + c.getResponseCode());
        try (InputStream in = c.getInputStream()) {
            ByteArrayOutputStream b = new ByteArrayOutputStream();
            byte[] buf = new byte[4096];
            for (int n; (n = in.read(buf)) > 0; ) b.write(buf, 0, n);
            return parse(b.toString("UTF-8"));
        } finally {
            c.disconnect();
        }
    }

    private Lookup() {}
}
