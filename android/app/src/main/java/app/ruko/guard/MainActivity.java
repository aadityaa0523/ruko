package app.ruko.guard;

import android.app.Activity;
import android.app.NotificationManager;
import android.app.role.RoleManager;
import android.content.Intent;
import android.graphics.Color;
import android.graphics.Typeface;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.view.Gravity;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;

import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;

public class MainActivity extends Activity {
    private static final int REQ_ROLE = 1;
    private TextView status;

    @Override
    protected void onCreate(Bundle b) {
        super.onCreate(b);
        // Shared from another app (SMS, WhatsApp): send it straight to the checker.
        Intent in = getIntent();
        if (Intent.ACTION_SEND.equals(in.getAction()) && in.getStringExtra(Intent.EXTRA_TEXT) != null) {
            String text = in.getStringExtra(Intent.EXTRA_TEXT);
            open("/check/?text=" + URLEncoder.encode(text.length() > 4000 ? text.substring(0, 4000) : text, StandardCharsets.UTF_8));
            finish();
            return;
        }

        LinearLayout col = new LinearLayout(this);
        col.setOrientation(LinearLayout.VERTICAL);
        int pad = dp(24);
        col.setPadding(pad, dp(48), pad, pad);

        TextView title = text("Ruko", 34, true);
        title.setTextColor(Color.parseColor("#1d55e6"));
        col.addView(title);
        col.addView(text("Warns you before you pick up a call from a number other people have reported as a scam.", 18, false));

        status = text("", 16, true);
        status.setPadding(0, dp(20), 0, dp(8));
        col.addView(status);

        col.addView(button("Turn on caller warnings", v -> requestRole()));
        col.addView(button("Protect a call now (speakerphone)", v -> open("/app/")));
        col.addView(button("Check a message, link or number", v -> open("/check/")));
        col.addView(button("Family Shield", v -> open("/account/")));

        TextView note = text("Ruko only sees the number of calls from people not in your contacts. It never blocks calls, "
                + "never reads your contacts or SMS, and can't hear calls: Android doesn't allow that. "
                + "To check what a caller says, put the call on speaker and open “Protect a call now”.", 14, false);
        note.setTextColor(Color.parseColor("#4b5567"));
        note.setPadding(0, dp(20), 0, 0);
        col.addView(note);

        ScrollView sv = new ScrollView(this);
        sv.setBackgroundColor(Color.parseColor("#f6f7fb"));
        sv.addView(col);
        setContentView(sv);

        RukoScreeningService.ensureChannels(getSystemService(NotificationManager.class));
        if (Build.VERSION.SDK_INT >= 33) requestPermissions(new String[]{"android.permission.POST_NOTIFICATIONS"}, 2);
    }

    @Override
    protected void onResume() {
        super.onResume();
        if (status == null) return;
        boolean on = getSystemService(RoleManager.class).isRoleHeld(RoleManager.ROLE_CALL_SCREENING);
        status.setText(on ? "Caller warnings are on." : "Caller warnings are off.");
        status.setTextColor(Color.parseColor(on ? "#0e7a4b" : "#d32f2f"));
    }

    private void requestRole() {
        RoleManager rm = getSystemService(RoleManager.class);
        if (rm.isRoleAvailable(RoleManager.ROLE_CALL_SCREENING) && !rm.isRoleHeld(RoleManager.ROLE_CALL_SCREENING)) {
            startActivityForResult(rm.createRequestRoleIntent(RoleManager.ROLE_CALL_SCREENING), REQ_ROLE);
        }
    }

    private void open(String path) {
        startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse(Lookup.SITE + path)));
    }

    private TextView text(String s, int sp, boolean bold) {
        TextView t = new TextView(this);
        t.setText(s);
        t.setTextSize(sp);
        t.setTextColor(Color.parseColor("#0f172a"));
        if (bold) t.setTypeface(Typeface.DEFAULT_BOLD);
        t.setPadding(0, dp(6), 0, dp(6));
        return t;
    }

    private Button button(String s, android.view.View.OnClickListener l) {
        Button btn = new Button(this);
        btn.setText(s);
        btn.setAllCaps(false);
        btn.setTextSize(17);
        btn.setGravity(Gravity.CENTER);
        btn.setMinHeight(dp(56));
        btn.setOnClickListener(l);
        LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT);
        lp.topMargin = dp(10);
        btn.setLayoutParams(lp);
        return btn;
    }

    private int dp(int v) {
        return Math.round(v * getResources().getDisplayMetrics().density);
    }
}
