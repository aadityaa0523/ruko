package app.ruko.guard;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Intent;
import android.net.Uri;
import android.telecom.Call;
import android.telecom.CallScreeningService;

/**
 * Android hands us each incoming call from a number that isn't in the contacts, before it rings.
 * Ruko never blocks or rejects: it lets the call ring and, if the community has reported the number,
 * shows a warning. Android does not let apps hear the call itself (see docs/ANDROID_PLAN.md).
 */
public class RukoScreeningService extends CallScreeningService {
    static final String CH_WARN = "scam_warning";
    static final String CH_NUDGE = "unknown_caller";

    @Override
    public void onScreenCall(Call.Details details) {
        // Answer at once so the ring is never delayed; the lookup runs alongside it.
        respondToCall(details, new CallResponse.Builder().build());
        if (details.getCallDirection() != Call.Details.DIRECTION_INCOMING || details.getHandle() == null) return;
        final String number = Lookup.normalize(details.getHandle().getSchemeSpecificPart());
        if (number.length() < 6) return;
        new Thread(() -> {
            Lookup.Result r;
            try { r = Lookup.fetch(number); } catch (Exception e) { r = null; }
            if (r != null && r.flagged()) {
                notify(CH_WARN, 1, "Warning: likely scam call",
                        pretty(number) + " was reported by " + r.reports + " people as " + Lookup.label(r.category)
                                + ". Don't share an OTP or send money. Tap to protect this call.");
            } else {
                notify(CH_NUDGE, 2, "Unknown caller: " + pretty(number),
                        "If they talk about money, police, KYC or a parcel, put it on speaker and tap here.");
            }
        }).start();
    }

    private void notify(String channel, int id, String title, String text) {
        NotificationManager nm = getSystemService(NotificationManager.class);
        ensureChannels(nm);
        Intent open = new Intent(Intent.ACTION_VIEW, Uri.parse(Lookup.SITE + "/app/"));
        PendingIntent pi = PendingIntent.getActivity(this, id, open, PendingIntent.FLAG_IMMUTABLE | PendingIntent.FLAG_UPDATE_CURRENT);
        Notification n = new Notification.Builder(this, channel)
                .setSmallIcon(android.R.drawable.stat_sys_warning)
                .setContentTitle(title)
                .setContentText(text)
                .setStyle(new Notification.BigTextStyle().bigText(text))
                .setCategory(Notification.CATEGORY_CALL)
                .setContentIntent(pi)
                .setAutoCancel(true)
                .setTimeoutAfter(5 * 60 * 1000)
                .build();
        nm.notify(id, n);
    }

    static void ensureChannels(NotificationManager nm) {
        nm.createNotificationChannel(new NotificationChannel(CH_WARN, "Scam call warnings", NotificationManager.IMPORTANCE_HIGH));
        nm.createNotificationChannel(new NotificationChannel(CH_NUDGE, "Unknown caller reminders", NotificationManager.IMPORTANCE_LOW));
    }

    static String pretty(String n) {
        return n.length() == 10 ? n.substring(0, 5) + " " + n.substring(5) : n;
    }
}
