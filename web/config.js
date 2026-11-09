// Public browser config. The Supabase publishable key is meant to be public; row-level security protects the data.
window.RUKO_CONFIG = {
  supabaseUrl: "https://izxqlbipvrtnsvpwekaw.supabase.co",
  supabaseKey: "sb_publishable_M8we6sPJuWsmIZOZuKQbrQ_pivd7C1I",
};

// Insert a row through Supabase's REST API (used by pages that don't load the full SDK).
async function sbInsert(table, row) {
  const c = window.RUKO_CONFIG;
  const r = await fetch(`${c.supabaseUrl}/rest/v1/${table}`, {
    method: "POST",
    headers: { apikey: c.supabaseKey, Authorization: `Bearer ${c.supabaseKey}`, "Content-Type": "application/json", Prefer: "return=minimal" },
    body: JSON.stringify(row),
  });
  if (!r.ok) throw new Error(`save failed (${r.status})`);
}
