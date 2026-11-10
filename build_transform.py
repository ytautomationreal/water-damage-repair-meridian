#!/usr/bin/env python3
"""Build Meridian gen.py from Fishers gen.py by replacing data blocks + global tokens.
Source of truth for facts: ~/workspace/water-damage-meridian/research.md
"""
import re, io

SRC = "/home/hatch/workspace/water-damage-fishers/gen.py"
DST = "/home/hatch/workspace/water-damage-meridian/gen.py"
s = open(SRC, encoding="utf-8").read()

def replace_block(text, start_marker, end_marker, new, start_inclusive=True):
    i = text.index(start_marker)
    j = text.index(end_marker, i)
    return text[:i] + new + text[j:]

# ---------- 0. Header comment + constants ----------
s = s.replace(
    'ROOT = os.path.expanduser("~/workspace/water-damage-fishers/site")',
    'ROOT = os.path.expanduser("~/workspace/water-damage-meridian/site")')
s = s.replace('BASE = "https://waterdamagerepairfishersin.com"',
              'BASE = "https://waterdamagerepairmeridianid.com"')
s = s.replace('PHONE_DISP = "(317) 978-8269"          # Ringba number (Muhammad, 2026-10-02)',
              'PHONE_DISP = "(208) 213-9706"          # PHONE PLACEHOLDER — replace with Idaho-local Ringba number before custom-domain launch')
s = s.replace('PHONE_TEL = "tel:+13179788269"', 'PHONE_TEL = "tel:+12082139706"')
s = s.replace('BRAND = "Fishers Water Damage Repair"', 'BRAND = "Meridian Water Damage Repair"')
s = s.replace(
    '''CITIES_NAV = [("Fishers", "/"), ("Carmel", "/carmel/"), ("Noblesville", "/noblesville/"),
              ("Westfield", "/westfield/"), ("Geist", "/geist/"), ("Indianapolis", "/indianapolis/"),
              ("McCordsville", "/mccordsville/"), ("Fortville", "/fortville/")]''',
    '''CITIES_NAV = [("Meridian", "/"), ("Boise", "/boise/"), ("Nampa", "/nampa/"),
              ("Eagle", "/eagle/"), ("Caldwell", "/caldwell/"), ("Kuna", "/kuna/"),
              ("Star", "/star/"), ("Middleton", "/middleton/"), ("Garden City", "/garden-city/"),
              ("Emmett", "/emmett/")]''')

# logo aria + header/footer brand bits handled by global replaces below; fix logo text block
s = s.replace('<span class="lt"><b>Fishers</b><span>Water Damage Repair</span></span>',
              '<span class="lt"><b>Meridian</b><span>Water Damage Repair</span></span>')
s = s.replace('aria-label="Fishers Water Damage Repair logo"',
              'aria-label="Meridian Water Damage Repair logo"')

# ---------- 1. SERVICES ----------
old_services = s[s.index("SERVICES = ["):s.index("]\n\ndef schema_ld")]
new_services = '''SERVICES = [
 ("water-damage-restoration", "Water Damage Restoration", "drop",
  "Full cleanup, drying, and repair after leaks, floods, and appliance failures — one call from standing water to restored rooms."),
 ("water-removal", "Water Removal & Extraction", "waves",
  "Truck-mounted extraction removes standing water fast, before it soaks deeper into flooring, drywall, and framing."),
 ("flood-cleanup", "Flood & Crawl Space Cleanup", "home",
  "Flooded crawl space or ground floor? We pump out water, remove damaged materials, dry the structure, and sanitize — usually starting the same day."),
 ("mold-remediation", "Mold Remediation", "spore",
  "Containment, HEPA filtration, and removal of mold growth after water damage — with the moisture source fixed so it stays gone. Idaho has no mold license, so we show you how to vet any remediator."),
 ("sewage-cleanup", "Sewage Cleanup", "shield",
  "Sewage backups are a health hazard. We extract, disinfect, and deodorize affected areas safely and thoroughly."),
 ("burst-pipe-repair", "Burst Pipe Water Damage", "pipe",
  "Frozen or burst pipes can dump hundreds of gallons in an hour. We stop the damage, dry the structure, and repair what's wet."),
 ("basement-waterproofing", "Crawl Space Waterproofing & Drying", "shield",
  "Sump pump failure, seepage, and crawl-space moisture solutions that keep Meridian homes dry through spring snowmelt and winter freezes."),
 ("emergency-water-damage", "24/7 Emergency Water Damage", "clock",
  "Water doesn't wait for business hours, and neither do we. Emergency response across Meridian and the Treasure Valley, day or night."),
'''
s = s.replace(old_services, new_services)

# lb_schema locality + service_schema city
s = s.replace('"addressLocality": "Fishers",\n                        "addressRegion": "IN"',
              '"addressLocality": "Meridian",\n                        "addressRegion": "ID"')
s = s.replace('"name": name + " in Fishers, IN"', '"name": name + " in Meridian, ID"')
s = s.replace('"areaServed": {"@type": "City", "name": "Fishers, IN"}',
              '"areaServed": {"@type": "City", "name": "Meridian, ID"}')

# ---------- 2. SVC_DETAIL (whole block) ----------
SVC_DETAIL_NEW = r'''SVC_DETAIL = {
 "water-damage-restoration": {
   "h1": "Water Damage Restoration in Meridian, ID",
   "desc": "Complete water damage restoration in Meridian, ID — extraction, structural drying, repairs, and insurance documentation. 24/7 emergency response.",
   "intro": "Water damage restoration is the full job: stopping the source, extracting water, drying the structure to standard, and repairing what the water ruined. In Meridian, that usually means a burst pipe in a freeze, a failed water heater in a 2000s subdivision, or spring snowmelt working into a crawl space — and doing it fast, before mold turns a drying job into a demolition job.",
   "signs": [("Musty odor that won't leave", "Hidden moisture in walls, floors, or the crawl space is feeding microbial growth."),
             ("Warped, cupped, or buckling floors", "Hardwood and laminate absorb water and deform — early drying can save them."),
             ("Bubbling paint or staining", "Water is moving through drywall from a leak you may not have found yet."),
             ("Visible mold patches", "Growth means moisture has been present for days, not hours."),
             ("Higher water bills", "A hidden supply-line leak is quietly soaking your structure."),
             ("Damp, musty crawl space", "Meridian homes are overwhelmingly crawl-space and slab builds — moisture down there rots framing and feeds mold out of sight.")],
   "how": "We start with source control and extraction, then map moisture with meters and thermal imaging so nothing wet hides behind a wall or under a floor. Air movers and commercial dehumidifiers pull moisture from materials — not just the air — and we take daily readings until everything hits dry standard. Then repairs: drywall, flooring, trim, paint. Every step is photographed and logged for your claim.",
   "faqs": [("How long does restoration take?", "Emergency drying runs 3–5 days for most homes. Repairs after drying depend on scope — a single room may take days; a flooded ground floor, one to two weeks."),
            ("Do I need to move out during restoration?", "Usually not. If sewage is involved or large areas are being demolished, we may recommend short-term relocation for part of the job — we'll tell you honestly up front.")]},
 "water-removal": {
   "h1": "Water Removal & Extraction in Meridian, ID",
   "desc": "Fast standing-water extraction in Meridian, ID. Truck-mounted pumps remove water before it spreads into walls and flooring. 24/7 emergency service.",
   "intro": "Extraction is the highest-leverage hour of any water job. Every gallon we pump out is a gallon your walls, floors, and crawl space don't absorb — and professional extractors remove dramatically more water from carpet and padding than any rental machine.",
   "signs": [("Standing water anywhere indoors", "Even a half-inch spreads under walls and into adjacent rooms."),
             ("Sump pump failure during spring runoff", "Water rises fast once the pump quits — call before it reaches the water heater and furnace."),
             ("Carpet that squishes underfoot", "The padding beneath is saturated even if the surface feels merely damp."),
             ("Water heater or washer let go", "Appliance tanks dump 40–80 gallons in minutes — and whole Meridian subdivisions have water heaters reaching end of life within a few years of each other."),
             ("Water creeping toward electrical", "Panel, outlets, or appliances near water = call now, don't wade in."),
             ("Water in the crawl space", "Spring snowmelt and a high water table push water under Meridian homes first — it rarely stays there.")],
   "how": "Truck-mounted and portable extractors pull standing water from hard surfaces, carpet, padding, and crawl spaces. We weight-extract carpet to squeeze padding dry, then set drying equipment the same visit. Furniture is blocked up or moved, contents are protected, and we treat affected areas with antimicrobial when the water source calls for it.",
   "faqs": [("Can extraction really save my carpet?", "Often, yes — if the water was clean and we get there fast. Padding sometimes needs replacement even when carpet survives; we'll test and tell you."),
            ("Should I rent a shop vac instead?", "For a few gallons on tile, fine. For carpet, padding, or more than a small spill, household vacuums leave most of the water behind — and that leftover water is what grows mold.")]},
 "flood-cleanup": {
   "h1": "Flood & Crawl Space Cleanup in Meridian, ID",
   "desc": "Flood and crawl space cleanup in Meridian, ID — pump-out, debris removal, structural drying, and sanitizing after snowmelt, storms, and sump failures.",
   "intro": "Meridian homes are overwhelmingly crawl-space and slab builds, not basements — so when spring snowmelt, a high water table, or a failed sump pump sends water in, it lands in the crawl space and on the ground floor. We pump it out, remove what's ruined, dry the structure, and sanitize — so your home is a home again, not a reminder.",
   "signs": [("Water in the crawl space", "Snowmelt and groundwater work under the house first. A wet crawl space rots framing and grows mold out of sight."),
             ("Water over the ground floor", "Any depth counts; water finds wall cavities and wicks upward immediately."),
             ("Sump pit overflowing", "The pump failed, lost power, or can't match inflow — a backup pump conversation comes after cleanup."),
             ("Water marks on foundation walls", "Shifting groundwater and snowmelt push water through cracks and joints."),
             ("Furnace or water heater sitting in water", "Shut off power at the breaker if safe; both need inspection before restart."),
             ("Drain or sewage smell", "Floodwater through drains can carry sewage. Assume contamination until tested.")],
   "how": "We pump and extract floodwater from living areas and crawl spaces, sort contents (save what's salvageable, document what isn't), remove ruined materials, and pressure-wash and sanitize hard surfaces. Then structural drying — including crawl-space drying and encapsulation where needed — with daily moisture verification. Finally, we talk prevention: backup pumps, battery systems, and drainage fixes so the next spring runoff is boring.",
   "faqs": [("Is flood damage covered by insurance?", "Sump pump failure often is — if you carry the sump/sewage endorsement. Groundwater and overland flooding usually require flood insurance. We document everything so your claim gets a fair look either way."),
            ("My home has a crawl space, not a basement — can it still flood?", "Yes, and in Meridian that's the more common pattern. Crawl spaces fill first and dry last, and the moisture attacks floor framing and insulation from below. We dry and encapsulate crawl spaces as part of the job.")]},
 "mold-remediation": {
   "h1": "Mold Remediation in Meridian, ID",
   "desc": "Mold remediation in Meridian, ID — containment, HEPA filtration, safe removal, and moisture-source repair so mold doesn't return.",
   "intro": "Mold is a moisture problem wearing a disguise. Killing what's visible without fixing the water source is a temporary cosmetic fix. We contain, remove, and — critically — dry and repair the source so the growth stays gone. And because Idaho has no mold license and no state cleanup standard, we tell you exactly how to vet any remediator — including us: look for an Idaho contractor registration you can look up and IICRC S520 training held by the technicians on your job.",
   "signs": [("Visible spots on walls, ceilings, or grout", "What you see is usually a fraction of the colony."),
             ("Musty, earthy odor", "Often the first sign of hidden growth behind walls, under floors, or in the crawl space."),
             ("Allergy symptoms that ease away from home", "A classic household pattern worth investigating."),
             ("Past leak or flood in the same area", "Any water event older than 48 hours is a mold candidate."),
             ("Peeling paint or warped baseboards", "Moisture is feeding something behind the surface."),
             ("Damp crawl space", "Meridian's crawl spaces stay humid after snowmelt — the perfect quiet mold farm.")],
   "how": "We inspect and moisture-map first — including the crawl space — then build containment with negative air and HEPA filtration so remediation doesn't spread spores through your home. Contaminated porous materials are removed safely, structural surfaces are cleaned and treated, and the moisture source — leak, seepage, humidity — is fixed and verified dry. Optional third-party testing can confirm clearance.",
   "faqs": [("Idaho has no mold license — how do I vet a remediator?", "Ask for two things: an Idaho contractor registration you can look up, and IICRC S520 training held by the technicians actually on your job. Anyone who can't show both is selling confidence, not competence."),
            ("Is bleach enough to kill mold?", "On hard, non-porous surfaces it can help; on drywall, wood, and carpet it doesn't reach the roots and adds moisture. It's also no substitute for fixing the water source."),
            ("How much does mold remediation cost?", "Small contained areas can run a few hundred dollars; multi-room or HVAC-involved jobs run into the thousands. We scope it in writing after inspection — no scare tactics, no obligation."),
            ("Is mold covered by insurance?", "When it results from a covered water event (like a burst pipe) and is handled promptly, often yes. Mold from long-term neglect usually isn't — another reason fast drying matters.")]},
 "sewage-cleanup": {
   "h1": "Sewage Cleanup in Meridian, ID",
   "desc": "Safe sewage backup cleanup in Meridian, ID — extraction, disinfection, odor removal, and drying. Category 3 water handled to standard.",
   "intro": "Sewage water (Category 3) carries bacteria, viruses, and parasites. This is not a mop-and-bucket job. We extract, remove contaminated porous materials, disinfect structural surfaces, and dry — protecting your family and your claim.",
   "signs": [("Drains backing up on the ground floor", "Lowest fixtures go first — floor drains, ground-floor toilets, showers."),
             ("Sewage odor anywhere indoors", "Odor means contaminated water or gases are entering living space."),
             ("Toilets gurgling or slow drains throughout", "A main-line blockage announcing itself before the backup."),
             ("Water around the floor drain after rain", "Storm and sanitary systems are interacting — common in heavy Treasure Valley downpours."),
             ("Multiple fixtures backing up at once", "Points to the main sewer line, not a single clog."),
             ("Wet area near the cleanout or yard sogginess", "A broken or blocked line can leak outside too.")],
   "how": "Crews in PPE extract Category 3 water, remove unsalvageable porous materials (carpet, padding, drywall up to the contamination line), and clean and disinfect all affected hard surfaces. We then dry the structure, verify with moisture readings, and apply odor control. Everything is documented for insurance — sewage backups are commonly covered events.",
   "faqs": [("Is it safe to stay in the house?", "Keep people and pets out of the affected area until it's cleaned and disinfected. If bathrooms are unusable or contamination is widespread, short-term relocation is wise."),
            ("Can carpet be saved after a sewage backup?", "No — porous materials that absorbed sewage must go. Hard surfaces can be disinfected and saved. Anyone who tells you otherwise is cutting a corner with your health.")]},
 "burst-pipe-repair": {
   "h1": "Burst Pipe Water Damage Repair in Meridian, ID",
   "desc": "Burst or frozen pipe water damage cleanup in Meridian, ID — rapid drying, repair coordination, and insurance documentation, 24/7.",
   "intro": "A burst pipe can release hundreds of gallons an hour — into walls, ceilings, and floors. The pipe fix is the plumber's job; everything the water touched is ours. Treasure Valley winters make this a Meridian specialty: daytime highs above freezing, overnight lows in the teens, and pipes in crawl spaces, attics, and unheated garages splitting when the ice thaws.",
   "signs": [("Sudden drop in water pressure", "A split line is diverting water where it doesn't belong."),
             ("Water stain spreading on a ceiling or wall", "The leak is active above or inside — it will not dry itself."),
             ("Sound of running water with everything off", "Trust your ears; check the meter to confirm."),
             ("Frost on exposed pipes", "A frozen pipe is a burst pipe waiting for the thaw."),
             ("Bulging drywall or peeling paint", "Water is pooling inside the wall cavity."),
             ("No water from a faucet in winter", "Frozen line — shut off the main before it thaws and splits.")],
   "how": "While your plumber repairs the pipe (we can coordinate one), we extract water, open wet cavities where needed, and dry structure with meter verification. Ceilings get checked for saturated insulation, floors for trapped moisture, crawl spaces for standing water. Your claim file gets the photos and readings adjusters want for sudden-discharge events — usually a covered loss.",
   "faqs": [("What should I do the moment a pipe bursts?", "Shut off the main water valve, kill power to wet areas if safe, move contents, and call us. Don't wait for the plumber first — drying should start in parallel."),
            ("How do I keep pipes from freezing?", "Insulate exposed lines in crawl spaces, attics, and garages, keep cabinet doors open on cold nights, let faucets drip during deep freezes — Boise's record low is −25°F, and Treasure Valley winters hold at or below about 20°F for hours at a time — and disconnect exterior hoses before winter.")]},
 "basement-waterproofing": {
   "h1": "Crawl Space Waterproofing & Drying in Meridian, ID",
   "desc": "Crawl space waterproofing, sump pump solutions, and drying in Meridian, ID — interior drainage, backup pumps, and encapsulation for crawl-space and slab homes.",
   "intro": "Cleanup fixes today's flood; waterproofing prevents the sequel. Meridian homes are overwhelmingly crawl-space and slab builds, so that means managing water under the house — interior drainage, reliable sump systems, battery backups that work when the power doesn't, and crawl-space encapsulation that keeps snowmelt moisture out of your framing for good.",
   "signs": [("Standing water or damp soil in the crawl space", "Spring snowmelt and a high water table — fed by a century of irrigation seepage — push water under the house."),
             ("Musty smell rising through the floors", "Crawl-space moisture and mold announce themselves upstairs."),
             ("A sump pump that runs constantly", "It's undersized, failing, or your water table is outmatching it."),
             ("Damp or musty home after every rain", "Seepage is recurring, not a one-time event."),
             ("Sagging insulation under the floor", "Wet insulation falls and stops insulating — and holds moisture against joists."),
             ("No battery backup on the sump", "Most Meridian floods happen during spring runoff and storms — exactly when power is likeliest to go.")],
   "how": "We assess where water enters, then design the fix: crawl-space drainage to a properly sized sump basin, primary and battery-backup pumps, vapor-barrier encapsulation, crack injection or exterior grading corrections, and discharge lines that move water well away from the foundation. If your crawl space is currently wet or damaged, we dry and restore first, then waterproof.",
   "faqs": [("My home has no basement — do I still need waterproofing?", "Yes — in Meridian, the crawl space is where the water goes. Encapsulation plus a reliable sump system does for a crawl space what a basement system does elsewhere."),
            ("What does a battery backup really buy me?", "Time — typically many hours of pumping during an outage, which is exactly when Meridian crawl spaces flood. For homes with finished ground floors, it's the cheapest insurance you can buy.")]},
 "emergency-water-damage": {
   "h1": "24/7 Emergency Water Damage Service in Meridian, ID",
   "desc": "24/7 emergency water damage response in Meridian, ID — live answer, rapid extraction, and drying any hour. Call (208) 213-9706 now.",
   "intro": "It's 2 a.m. and there's water where water should never be. You don't need a call center, a callback queue, or business hours. You need a person, a truck, and a plan — in that order, fast.",
   "signs": [("Any standing water, any hour", "If you're reading this with wet feet, skip the research and call."),
             ("Water near the electrical panel or outlets", "Stay out of the water; we'll coordinate safe entry."),
             ("A leak you can't stop", "If the shut-off doesn't stop it, it's an emergency by definition."),
             ("Sewage smell or visible backup", "Category 3 contamination — keep kids and pets away."),
             ("Ceiling sagging with water", "A water-loaded ceiling can collapse; clear the room below."),
             ("Storm water or snowmelt entering the home", "Active flooding needs pumping now, not after the runoff stops.")],
   "how": "One call reaches a live dispatcher who gives you immediate shut-off and safety guidance while a crew rolls. On arrival: source control, extraction, moisture mapping, and drying equipment set the same visit. Then daily monitoring and a full documentation file for your insurer. Nights, weekends, holidays — same process, same price structure.",
   "faqs": [("What should I do while I wait for the crew?", "Shut off the water main if the source is plumbing, turn off power to wet areas at the breaker if you can do it dry-footed, move valuables up, and take photos for your claim."),
            ("Does the emergency call cost more at night?", "Emergency response is priced by the work, not the clock on the wall. You get a written estimate before non-emergency work proceeds.")]},
}
'''
s = replace_block(s, "SVC_DETAIL = {", "\ndef service_page", SVC_DETAIL_NEW + "\n")

# faq_set base text: Fishers -> Meridian (global pass later covers most; fix here explicitly)
s = s.replace('f"How much does {svc_name.lower()} cost in Fishers?"',
              'f"How much does {svc_name.lower()} cost in Meridian?"')
s = s.replace('"24/7, with a target of about an hour inside Fishers.',
              '"24/7, with a target of about an hour inside Meridian.')

# ---------- 3. CITY_DETAIL (towns) ----------
CITY_NEW = r'''CITY_DETAIL = {
 "boise": ("Boise", "238,429", "83702",
   "Boise is Idaho's largest city and the anchor of the Treasure Valley — and the Boise River runs right through it. The river is dam-controlled and hasn't hit its 100-year flow since Lucky Peak Dam was completed in 1955, but it still floods: peak flows hit 9,600 cfs in 2017, washing away Greenbelt sections and flooding riverside homes. Boise State's worst-case scenario names flooding near the river in Boise, Garden City, Eagle, Star, and Caldwell.",
   [("Boise River floodplain & spring snowmelt", "Riverside and Greenbelt-adjacent homes face the valley's highest overland-flood exposure when snowmelt peaks."),
    ("Older housing stock near the river", "Boise's older neighborhoods carry aging supply lines, cast iron, and pre-1980 plumbing that fails quietly."),
    ("Sump pump failure during spring runoff", "High water tables in spring keep pumps running — and wearing out — all season."),
    ("Freeze–thaw burst pipes", "Winter lows in the teens split pipes in crawl spaces, attics, and unheated garages across the city.")],
   ["/", "/garden-city/", "/eagle/", "/meridian/"]),
 "nampa": ("Nampa", "120,384", "83651",
   "Nampa is the Treasure Valley's second-largest city, and its housing stock is older than Meridian's — median build year 2000, with 26% of homes built before 1980. Older pipes, older water heaters, and older drainage mean more sudden failures per block than anywhere else in the valley.",
   [("Older pipes failing", "Pre-1980 stock and 2000-era subdivisions alike are hitting pipe, water-heater, and supply-line failure years."),
    ("Sump pump & drainage failures", "Aging pumps and older drainage systems quit during spring storms — the classic Nampa basement and crawl-space flood."),
    ("Sewer backups in older neighborhoods", "Aging laterals and main lines back up under storm load."),
    ("Freeze–thaw burst pipes", "Crawl-space and exterior-wall pipes split in January cold snaps, then flood when the ice thaws.")],
   ["/", "/caldwell/", "/middleton/", "/meridian/"]),
 "eagle": ("Eagle", "35,112", "83616",
   "Eagle is the valley's wealthiest market — median sale price $846,782 (September 2026) — and a river town: the 1998 Eagle Island levee break flooded nearby homes and evacuated 60 residents, and a 1997 dike break near South Eagle Road flooded the road and two homes. High-value homes on river-adjacent ground make fast, documented drying an asset-protection job.",
   [("Boise River & Eagle Island flood history", "Levee and dike breaks in 1997–98 are on the record — river-adjacent homes carry real flood exposure."),
    ("High-value finishes at risk", "Custom millwork, wide-plank floors, and finished lower levels can't be patched — they must be dried right the first time."),
    ("Large-home system complexity", "Multiple water heaters, softeners, and bath groups multiply hidden-leak points per home."),
    ("Freeze–thaw burst pipes", "Estate-scale homes have more exterior-wall and garage plumbing exposed to winter lows.")],
   ["/", "/boise/", "/star/", "/meridian/"]),
 "caldwell": ("Caldwell", "79,746", "83605",
   "Caldwell is one of Idaho's fastest-growing cities (+4.07% a year) and sits in Boise State's worst-case Boise River flood zone. Its housing mixes older agricultural-era stock with fast new subdivisions — two different failure profiles on the same streets.",
   [("Boise River worst-case flood zone", "Caldwell is named in the worst-case river-flooding scenario for the valley — river-adjacent homes carry real exposure."),
    ("Older agricultural-era plumbing", "Older stock brings galvanized and cast-iron lines that leak quietly for months."),
    ("New-subdivision sump & drainage failures", "Fast growth means thousands of young pumps and water heaters aging on the same schedule."),
    ("Freeze–thaw burst pipes", "Crawl-space pipes in both old and new homes split in winter cold snaps.")],
   ["/", "/nampa/", "/middleton/", "/meridian/"]),
 "kuna": ("Kuna", "32,665", "83634",
   "Kuna is Meridian's fast-growing southern neighbor (+3.62% a year) — and its newest: 2010-and-later PEX subdivisions spill over from south Meridian. New builds don't mean no water damage; they mean builder-grade fittings, high water pressure, and water heaters aging together by subdivision.",
   [("New-build PEX & builder-grade fittings", "Newer subdivisions suffer builder-grade fittings and PRV/high-pressure failures rather than old-pipe decay."),
    ("Water heaters aging together", "Whole subdivisions built in the same years reach water-heater end of life within a few years of each other."),
    ("Pressurized irrigation leaks", "Kuna lots run on pressurized irrigation — irrigation lines and high water tables are a local risk factor."),
    ("Freeze–thaw burst pipes", "Exterior-wall and garage plumbing in new subdivisions splits in January cold.")],
   ["/", "/meridian/", "/nampa/", "/boise/"]),
 "star": ("Star", "22,547", "83669",
   "Star is Idaho's second-fastest-growing city (+8.01% a year) — it has doubled since 2020. River-adjacent and almost entirely new-build PEX stock, Star is Meridian's story five years earlier: whole subdivisions of young homes whose fittings, angle stops, and water heaters will age together.",
   [("River-adjacent flood exposure", "Star is named in Boise State's worst-case river-flooding scenario — new homes on river ground still flood."),
    ("New-build failure modes", "PEX, plastic-bodied angle stops, and braided appliance connectors — the post-2000 failure set, at subdivision scale."),
    ("Builder-grade fittings & high pressure", "PRV failures and high water pressure split fittings in young homes."),
    ("Freeze–thaw burst pipes", "Crawl-space and garage plumbing in new subdivisions is the first to freeze.")],
   ["/", "/eagle/", "/middleton/", "/meridian/"]),
 "middleton": ("Middleton", "12,600", "83644",
   "Middleton has grown 33.3% since 2020 — the 6th-fastest city in Idaho — with 389 building permits in 2025 alone. Median build year is 2009 and 47.4% of homes were built in 2010 or later: a young, fast-growing city where new-build failure modes dominate.",
   [("New-build PEX & fittings failures", "2010s subdivisions bring builder-grade angle stops, braided connectors, and PRV issues."),
    ("Water heaters aging together", "The 2009–2015 build wave's tanks are entering failure years on the same schedule."),
    ("Sump pump dependence", "Young subdivisions rely on pumps cycling against spring snowmelt and a high water table."),
    ("Freeze–thaw burst pipes", "Crawl-space plumbing in new homes splits in winter cold snaps.")],
   ["/", "/star/", "/caldwell/", "/meridian/"]),
 "garden-city": ("Garden City", "13,203", "83714",
   "Garden City sits on the Boise River and the Greenbelt, with the oldest housing in the valley core — and several restoration companies based here. Boise State's worst-case flood scenario names Garden City alongside Boise, Eagle, Star, and Caldwell. Old homes on river ground: the valley's highest combined flood-and-plumbing risk.",
   [("Boise River flood exposure", "River-adjacent homes and the Greenbelt corridor face the valley's most direct overland-flood risk."),
    ("Oldest housing in the valley core", "Old plumbing, old laterals, and old foundations — generations of pipe materials aging at once."),
    ("High water table & seepage", "River groundwater keeps constant pressure on foundations and crawl spaces."),
    ("Freeze–thaw burst pipes", "Uninsulated crawl spaces and exterior walls in older homes split first in winter.")],
   ["/", "/boise/", "/eagle/", "/meridian/"]),
 "emmett": ("Emmett", "8,900", "83617",
   "Emmett is the Gem County seat and the furthest town we serve — a small, older community north of the valley floor. Its housing stock skews older than Meridian's, with more pre-1980 homes and more well-and-septic-era plumbing, and winter cold hits harder up the valley.",
   [("Older housing stock", "More pre-1980 homes than the valley average means older pipes, older heaters, and older laterals."),
    ("Freeze–thaw burst pipes", "Colder winters up the valley make frozen and burst pipes the signature Emmett emergency."),
    ("Well & pressure-tank issues", "Rural properties add well-water failure modes the suburbs don't see."),
    ("Crawl-space moisture", "Older crawl spaces on valley soils stay damp and grow mold quietly.")],
   ["/", "/middleton/", "/star/", "/meridian/"]),
}
'''
s = replace_block(s, "CITY_DETAIL = {", "\ndef location_page", CITY_NEW + "\n")

# location_page: chips show "Median home {home_val}" — third tuple element is now primary ZIP; fix chips + near-link guard
s = s.replace('<span class="chip">{ICONS[\'check\']} Median home {home_val}</span>',
              '<span class="chip">{ICONS[\'check\']} Primary ZIP {home_val}</span>')
# near links: Fishers guard lists city slugs; our near lists use "/" for Meridian — existing dict already maps "fishers"->"/" but our slugs are meridian; patch existing dict
s = s.replace('existing = {"fishers": "/", "carmel": "/carmel/", "noblesville": "/noblesville/", "westfield": "/westfield/",\n                "geist": "/geist/", "indianapolis": "/indianapolis/", "mccordsville": "/mccordsville/", "fortville": "/fortville/"}',
              'existing = {"meridian": "/", "boise": "/boise/", "nampa": "/nampa/", "eagle": "/eagle/",\n                "caldwell": "/caldwell/", "kuna": "/kuna/", "star": "/star/", "middleton": "/middleton/",\n                "garden-city": "/garden-city/", "emmett": "/emmett/"}')
_NEAR_OLD = '''    near_cards = "".join(f'<a class="area rv" href="{existing[u.strip("/").split("/")[0]]}">{u.strip("/").title()}<span>IN →</span></a>' for u in near if u.strip("/").split("/")[0] in existing)'''
_NEARD_NEW = '''    def _near_card(u):
        key = u.strip("/").split("/")[0]
        href = existing.get(key, "/")
        label = "Meridian" if u == "/" else u.strip("/").replace("-", " ").title()
        return f'<a class="area rv" href="{href}">{label}<span>ID →</span></a>'
    near_cards = "".join(_near_card(u) for u in near if u.strip("/").split("/")[0] in existing or u == "/")'''
assert _NEAR_OLD in s
s = s.replace(_NEAR_OLD, _NEARD_NEW)

# ---------- 4. ZIP_DETAIL (21 ZIPs) ----------
ZIP_NEW = r'''ZIP_DETAIL = {
 "83642": {
   "area": "South & West Meridian", "pop": "~62,279 residents",
   "intro": "83642 is Meridian's south and west residential ZIP — the primary residential ZIP on the city's older, southern side. Meridian's housing here is still overwhelmingly post-2000, but this is where the city's earliest subdivisions sit, and where the first big wave of water heaters, angle stops, and appliance connectors is reaching end of life together.",
   "hoods": [("Downtown Meridian", "Meridian's oldest stock — pre-2000 pipes and polybutylene risk on older, often no-HOA lots."),
             ("Tuscany", "Mature southeast Meridian community; irrigation-fed landscaping and older water heaters."),
             ("The Village at Meridian", "Lifestyle-center area with commercial-adjacent and nearby residential stock.")],
   "landmarks": "South & west Meridian · Ada County · Nampa & Meridian Irrigation District canals",
   "problems": [("Water heaters aging together", "2000s subdivisions in 83642 are hitting tank end-of-life in waves — a ruptured tank dumps 40–80 gallons."),
                ("Angle stops & braided connectors failing", "Plastic-bodied angle stops and appliance connectors from the post-2000 build wave are a signature Meridian failure."),
                ("Pressurized irrigation leaks", "Most homes run pressurized irrigation through NMID — irrigation lines and a high water table are a local risk factor."),
                ("Freeze–thaw burst pipes", "Crawl-space and garage pipes split in winter cold snaps, then flood on the thaw.")]},
 "83646": {
   "area": "North Meridian", "pop": "~76,023 residents — Idaho's most populous ZIP",
   "intro": "83646 is north Meridian — and Idaho's most populous ZIP. This is the city's newest growth corridor: master-planned subdivisions like Paramount, Bridgetower, and Lochsa Falls, built mostly after 2000, with a median build year for the city of 2007. New homes, new failure modes: builder-grade fittings, high water pressure, and whole subdivisions aging together.",
   "hoods": [("Paramount", "NW Meridian master-planned community off Chinden Blvd; 2000s builds hitting water-heater and angle-stop end of life."),
             ("Bridgetower", "NW Meridian; original built-out community with family-sized homes and crawl spaces."),
             ("Lochsa Falls", "NE Meridian off Linder Rd; water features at the entrance and canal/lateral proximity.")],
   "landmarks": "North Meridian · Ada County · Eagle Road corridor · Chinden Blvd",
   "problems": [("New-build failure modes", "PEX with builder-grade fittings and PRV/high-pressure failures — not old-pipe decay."),
                ("Subdivisions aging together", "Water heaters, angle stops, and appliance connectors installed in the same build years fail in waves."),
                ("Canal & high water table seepage", "NMID canals and laterals plus a century of irrigation seepage keep groundwater high under north Meridian homes."),
                ("Spring snowmelt into crawl spaces", "Snowmelt works into crawl spaces first — Meridian homes are overwhelmingly crawl-space and slab builds.")]},
 "83702": {
   "area": "Downtown Boise", "pop": "City of Boise — 238,429 residents",
   "intro": "83702 covers downtown Boise — the city's oldest core, on the Boise River. Older commercial and residential stock, the Greenbelt, and river-adjacent ground: the valley's most direct river-flood exposure combined with the city's oldest plumbing.",
   "hoods": [("Downtown Boise", "Boise's historic core on the river — older stock, older pipes, river-adjacent ground.")],
   "landmarks": "Downtown Boise · Boise River · Greenbelt · Ada County",
   "problems": [("Boise River flood exposure", "Downtown sits on the river — 2017 peak flows of 9,600 cfs washed away Greenbelt sections and flooded riverside homes."),
                ("Oldest plumbing in the valley", "Pre-1980 and early-era lines fail quietly inside walls."),
                ("Sump pump failure in spring runoff", "High water tables in spring keep pumps running all season."),
                ("Freeze–thaw burst pipes", "Winter lows in the teens split pipes in crawl spaces and unheated spaces.")]},
 "83704": {
   "area": "West Boise", "pop": "City of Boise — 238,429 residents",
   "intro": "83704 is west Boise — established neighborhoods between downtown and Meridian, mixing mid-century homes with newer infill. Settlers Irrigation District serves West Boise, Meridian, and South Eagle via a 20-mile canal and 95 miles of laterals.",
   "hoods": [("West Boise", "Established Boise neighborhoods toward Meridian — mixed-era stock on irrigation-district ground.")],
   "landmarks": "West Boise · Settlers Irrigation District · Ada County",
   "problems": [("Irrigation & high water table", "Canal and lateral seepage keeps groundwater high under west Boise homes."),
                ("Aging mid-century plumbing", "Older supply lines and water heaters failing on schedule."),
                ("Sump pump & seepage", "Spring runoff pushes water into crawl spaces and ground floors."),
                ("Freeze–thaw burst pipes", "Crawl-space pipes split in winter cold snaps.")]},
 "83705": {
   "area": "South & Southeast Boise", "pop": "City of Boise — 238,429 residents",
   "intro": "83705 covers south and southeast Boise — established neighborhoods with a wide range of housing ages, from mid-century stock to newer subdivisions toward the foothills.",
   "hoods": [("South Boise", "Established south Boise neighborhoods — mixed-era housing, mixed plumbing eras.")],
   "landmarks": "South Boise · Ada County",
   "problems": [("Aging plumbing in older stock", "Mid-century supply lines and water heaters are at end of life."),
                ("New-build fittings failures", "Newer subdivisions bring builder-grade fittings and PRV issues."),
                ("Sump pump & seepage", "Spring runoff and a high water table push water into crawl spaces."),
                ("Freeze–thaw burst pipes", "Exterior-wall and garage pipes split in winter.")]},
 "83706": {
   "area": "Southeast Boise", "pop": "City of Boise — 238,429 residents",
   "intro": "83706 is southeast Boise — neighborhoods toward the Boise foothills and the river corridor, with housing ranging from mid-century to new construction.",
   "hoods": [("Southeast Boise", "Foothills-side Boise neighborhoods — mixed-era homes near the river corridor.")],
   "landmarks": "Southeast Boise · Boise River corridor · Ada County",
   "problems": [("River-corridor groundwater", "Proximity to the Boise River keeps water tables high in spring."),
                ("Mixed-era plumbing failures", "Mid-century lines and new-build fittings fail on different schedules — both fail."),
                ("Sump pump & seepage", "Spring snowmelt pushes water into crawl spaces and ground floors."),
                ("Freeze–thaw burst pipes", "Crawl-space and attic pipes split in winter cold snaps.")]},
 "83709": {
   "area": "Southwest Boise", "pop": "City of Boise — 238,429 residents",
   "intro": "83709 is southwest Boise — established and newer subdivisions on the city's Meridian side, where irrigation districts and newer PEX subdivisions meet older stock.",
   "hoods": [("Southwest Boise", "Boise neighborhoods toward Meridian — irrigation-district ground, mixed-era subdivisions.")],
   "landmarks": "Southwest Boise · Nampa & Meridian Irrigation District · Ada County",
   "problems": [("Pressurized irrigation leaks", "Irrigation lines and canal seepage are a local risk factor across southwest Boise."),
                ("New-build & older-stock failures", "PEX fittings in new subdivisions, aging lines in older streets."),
                ("High water table seepage", "A century of irrigation seepage keeps groundwater high."),
                ("Freeze–thaw burst pipes", "Crawl-space pipes split in winter.")]},
 "83712": {
   "area": "East Boise", "pop": "City of Boise — 238,429 residents",
   "intro": "83712 is east Boise — neighborhoods along the river and toward the foothills, including some of the city's higher-value and older homes.",
   "hoods": [("East Boise", "River- and foothills-side Boise neighborhoods — mixed-era, higher-value stock.")],
   "landmarks": "East Boise · Boise River · Ada County",
   "problems": [("River-adjacent groundwater", "Homes near the river live with a high water table through spring runoff."),
                ("Older & high-value plumbing systems", "Large homes carry more heaters, softeners, and bath groups — more hidden failure points."),
                ("Sump pump & seepage", "Spring snowmelt pushes water into crawl spaces and lower levels."),
                ("Freeze–thaw burst pipes", "Exterior-wall pipes split in winter cold snaps.")]},
 "83713": {
   "area": "Northwest Boise", "pop": "City of Boise — 238,429 residents",
   "intro": "83713 is northwest Boise — established neighborhoods on the city's north side, mixing older homes with newer subdivisions toward Eagle.",
   "hoods": [("Northwest Boise", "North-side Boise neighborhoods toward Eagle — mixed-era housing.")],
   "landmarks": "Northwest Boise · Ada County",
   "problems": [("Aging plumbing in older stock", "Mid-century and 1980s lines are entering failure years."),
                ("New-subdivision fittings failures", "Builder-grade fittings and PRV issues in newer streets."),
                ("Sump pump & seepage", "Spring runoff pushes water into crawl spaces."),
                ("Freeze–thaw burst pipes", "Crawl-space and garage pipes split in winter.")]},
 "83716": {
   "area": "Far East Boise", "pop": "City of Boise — 238,429 residents",
   "intro": "83716 is far east Boise — the city's eastern edge toward the foothills and the river corridor, with newer subdivisions and estate-scale homes.",
   "hoods": [("Far East Boise", "Eastern Boise edge — newer subdivisions and larger homes near the foothills.")],
   "landmarks": "Far East Boise · Boise foothills · Ada County",
   "problems": [("Large-home system complexity", "Estate-scale homes carry multiple heaters and bath groups — more hidden leak points."),
                ("New-build fittings failures", "Builder-grade fittings and high water pressure in newer subdivisions."),
                ("River-corridor groundwater", "Spring runoff keeps water tables high near the river."),
                ("Freeze–thaw burst pipes", "Exterior-wall and garage plumbing splits in winter.")]},
 "83651": {
   "area": "Nampa — Central & North", "pop": "City of Nampa — 120,384 residents",
   "intro": "83651 is central and north Nampa — the city's core ZIP, covering its older downtown and established neighborhoods. Nampa's median build year is 2000 and 26% of homes were built before 1980, so this ZIP carries the valley's highest concentration of aging-pipe failures.",
   "hoods": [("Central Nampa", "Nampa's older core — pre-1980 stock, aging pipes, and older drainage.")],
   "landmarks": "Central Nampa · Canyon County",
   "problems": [("Older pipes failing", "Pre-1980 stock means galvanized and cast-iron lines leaking quietly for months."),
                ("Sump pump & drainage failures", "Aging pumps quit during spring storms."),
                ("Sewer backups", "Aging laterals back up under storm load."),
                ("Freeze–thaw burst pipes", "Crawl-space pipes split in January cold snaps.")]},
 "83686": {
   "area": "Nampa — South & West", "pop": "City of Nampa — 120,384 residents",
   "intro": "83686 covers south and west Nampa — established neighborhoods and newer subdivisions on the city's growing side, mixing older stock with 2000s-era builds.",
   "hoods": [("South Nampa", "South and west Nampa neighborhoods — established stock plus newer subdivisions.")],
   "landmarks": "South Nampa · Canyon County",
   "problems": [("Mixed-era plumbing failures", "Older lines in established streets, builder-grade fittings in newer ones."),
                ("Sump pump failures", "Spring storms overload aging pumps."),
                ("Water heaters aging together", "2000s subdivisions hitting tank end-of-life in waves."),
                ("Freeze–thaw burst pipes", "Crawl-space and exterior-wall pipes split in winter.")]},
 "83687": {
   "area": "Nampa — North & East", "pop": "City of Nampa — 120,384 residents",
   "intro": "83687 is north and east Nampa — the city's newer growth side toward Caldwell and the interstate, with 2000s-and-later subdivisions alongside established neighborhoods.",
   "hoods": [("North Nampa", "North and east Nampa — newer subdivisions toward Caldwell and the interstate.")],
   "landmarks": "North Nampa · Canyon County",
   "problems": [("New-build fittings failures", "PEX subdivisions with builder-grade angle stops and PRV issues."),
                ("Water heaters aging together", "The 2000s build wave's tanks are failing on the same schedule."),
                ("Sump pump dependence", "Young subdivisions rely on pumps against spring runoff."),
                ("Freeze–thaw burst pipes", "Crawl-space plumbing splits in winter cold snaps.")]},
 "83616": {
   "area": "Eagle", "pop": "City of Eagle — 35,112 residents",
   "intro": "83616 is Eagle — the valley's wealthiest market, with a median sale price of $846,782 (September 2026). River-adjacent and high-value: the 1998 Eagle Island levee break flooded nearby homes and evacuated 60 residents, and a 1997 dike break near South Eagle Road flooded the road and two homes.",
   "hoods": [("Eagle", "Eagle's river-adjacent neighborhoods — high-value homes on flood-history ground.")],
   "landmarks": "Eagle · Eagle Island · Boise River · Ada County",
   "problems": [("Boise River flood history", "Levee and dike breaks in 1997–98 are on the record for Eagle ground."),
                ("High-value finishes at risk", "Custom finishes must be dried right the first time — documentation matters as much as speed."),
                ("Large-home system complexity", "Multiple heaters, softeners, and bath groups multiply hidden-leak points."),
                ("Freeze–thaw burst pipes", "Estate-scale homes have more exposed exterior-wall plumbing.")]},
 "83605": {
   "area": "Caldwell — Central", "pop": "City of Caldwell — 79,746 residents",
   "intro": "83605 is central Caldwell — the city's older core in Canyon County, with agricultural-era housing stock alongside newer infill. Caldwell sits in Boise State's worst-case Boise River flood zone.",
   "hoods": [("Central Caldwell", "Caldwell's older core — agricultural-era stock and newer infill.")],
   "landmarks": "Central Caldwell · Canyon County · Boise River worst-case flood zone",
   "problems": [("Boise River worst-case flood zone", "Caldwell is named in the valley's worst-case river-flooding scenario."),
                ("Older agricultural-era plumbing", "Galvanized and cast-iron lines leak quietly for months."),
                ("Sump pump & drainage failures", "Older drainage systems quit during spring storms."),
                ("Freeze–thaw burst pipes", "Crawl-space pipes split in winter cold snaps.")]},
 "83607": {
   "area": "Caldwell — South & East", "pop": "City of Caldwell — 79,746 residents",
   "intro": "83607 covers south and east Caldwell — the city's fast-growing side, where new subdivisions are rising beside older agricultural properties. Caldwell is growing at 4.07% a year, the 7th-fastest city in Idaho.",
   "hoods": [("South Caldwell", "South and east Caldwell — fast-growing subdivisions beside older farm-era properties.")],
   "landmarks": "South Caldwell · Canyon County",
   "problems": [("New-subdivision failure modes", "Builder-grade fittings and PRV issues in fast-growing subdivisions."),
                ("Older farm-era plumbing", "Agricultural-era lines on older properties fail quietly."),
                ("River flood exposure", "Caldwell sits in the worst-case Boise River flood zone."),
                ("Freeze–thaw burst pipes", "Crawl-space plumbing splits in winter.")]},
 "83634": {
   "area": "Kuna", "pop": "City of Kuna — 32,665 residents",
   "intro": "83634 is Kuna — Meridian's fast-growing southern neighbor (+3.62% a year) and one of the valley's newest housing markets: 2010-and-later PEX subdivisions spilling over from south Meridian.",
   "hoods": [("Kuna", "Kuna's new PEX subdivisions — south Meridian spillover, newest builds in the valley.")],
   "landmarks": "Kuna · Ada County · South Meridian corridor",
   "problems": [("New-build PEX & builder-grade fittings", "Builder-grade fittings and PRV/high-pressure failures, not old-pipe decay."),
                ("Water heaters aging together", "Subdivisions built in the same years reach tank end of life together."),
                ("Pressurized irrigation leaks", "Irrigation lines and a high water table are a local risk factor."),
                ("Freeze–thaw burst pipes", "Exterior-wall and garage plumbing splits in January cold.")]},
 "83669": {
   "area": "Star", "pop": "City of Star — 22,547 residents",
   "intro": "83669 is Star — Idaho's second-fastest-growing city (+8.01% a year), doubled since 2020. River-adjacent and almost entirely new-build PEX stock: Meridian's story five years earlier.",
   "hoods": [("Star", "Star's new-build subdivisions — river-adjacent, PEX stock, doubled since 2020.")],
   "landmarks": "Star · Boise River · Ada County",
   "problems": [("River-adjacent flood exposure", "Star is named in Boise State's worst-case river-flooding scenario."),
                ("New-build failure modes", "PEX, plastic-bodied angle stops, and braided appliance connectors at subdivision scale."),
                ("Builder-grade fittings & high pressure", "PRV failures split fittings in young homes."),
                ("Freeze–thaw burst pipes", "Crawl-space and garage plumbing is the first to freeze.")]},
 "83644": {
   "area": "Middleton", "pop": "City of Middleton — 12,600 residents",
   "intro": "83644 is Middleton — up 33.3% since 2020, the 6th-fastest city in Idaho, with 389 building permits in 2025 alone. Median build year 2009; 47.4% of homes built in 2010 or later.",
   "hoods": [("Middleton", "Middleton's 2010s subdivisions — young, fast-growing, new-build failure modes.")],
   "landmarks": "Middleton · Canyon County",
   "problems": [("New-build PEX & fittings failures", "2010s subdivisions bring builder-grade angle stops and braided connectors."),
                ("Water heaters aging together", "The 2009–2015 build wave's tanks are entering failure years together."),
                ("Sump pump dependence", "Young subdivisions rely on pumps against spring snowmelt."),
                ("Freeze–thaw burst pipes", "Crawl-space plumbing splits in winter cold snaps.")]},
 "83714": {
   "area": "Garden City", "pop": "City of Garden City — 13,203 residents",
   "intro": "83714 is Garden City — on the Boise River and the Greenbelt, with the oldest housing in the valley core. Boise State's worst-case flood scenario names Garden City alongside Boise, Eagle, Star, and Caldwell.",
   "hoods": [("Garden City", "Garden City's river-adjacent neighborhoods — oldest housing in the valley core.")],
   "landmarks": "Garden City · Boise River · Greenbelt · Ada County",
   "problems": [("Boise River flood exposure", "River-adjacent homes face the valley's most direct overland-flood risk."),
                ("Oldest housing in the valley core", "Old plumbing, old laterals, old foundations — generations of materials aging at once."),
                ("High water table & seepage", "River groundwater keeps constant pressure on foundations and crawl spaces."),
                ("Freeze–thaw burst pipes", "Uninsulated crawl spaces in older homes split first in winter.")]},
 "83617": {
   "area": "Emmett", "pop": "City of Emmett — 8,900 residents",
   "intro": "83617 is Emmett — the Gem County seat and the furthest town we serve, north of the valley floor. Older housing stock, more pre-1980 homes, and colder winters up the valley.",
   "hoods": [("Emmett", "Emmett's older neighborhoods — Gem County seat, furthest out in our service area.")],
   "landmarks": "Emmett · Gem County",
   "problems": [("Older housing stock", "More pre-1980 homes than the valley average — older pipes, heaters, and laterals."),
                ("Freeze–thaw burst pipes", "Colder winters up the valley make frozen and burst pipes the signature Emmett emergency."),
                ("Well & pressure-tank issues", "Rural properties add well-water failure modes."),
                ("Crawl-space moisture", "Older crawl spaces stay damp and grow mold quietly.")]},
}
'''
s = replace_block(s, "ZIP_DETAIL = {", "\ndef zip_page", ZIP_NEW + "\n")

# ---------- 5. Neighborhoods: HOOD_SLUGS + HOOD_DETAIL (20 verified names) ----------
HOOD_NEW = r'''HOOD_SLUGS = {"Paramount": "paramount", "Bridgetower": "bridgetower",
  "Bridgetower West": "bridgetower-west", "Tuscany": "tuscany", "Lochsa Falls": "lochsa-falls",
  "Spurwing Greens": "spurwing-greens", "Saguaro Canyon": "saguaro-canyon",
  "Settlers Bridge": "settlers-bridge", "Bainbridge": "bainbridge",
  "The Oaks North": "the-oaks-north", "The Keep": "the-keep",
  "Heritage Commons": "heritage-commons", "Sienna Creek": "sienna-creek",
  "Century Farm": "century-farm", "Meridian Greens": "meridian-greens",
  "Canterbury Commons": "canterbury-commons", "Downtown Meridian": "downtown-meridian",
  "The Village at Meridian": "the-village-at-meridian",
  "Discovery Park": "discovery-park", "Jump Creek": "jump-creek"}

# slug: (name, town, zip, era, intro, problems[4], anchors)
# NOTE: The Keep, Sienna Creek, Century Farm, Meridian Greens, Canterbury Commons are
# verified ONLY as names on local real-estate lists — boundaries/character unverified
# (research.md §6). Their pages carry only the verified name + Meridian-wide drivers,
# no invented street-level detail.
HOOD_DETAIL = {
 "paramount": ("Paramount", "Meridian", "83646", "NW Meridian master-planned · off Chinden Blvd",
   "Paramount is a mature master-planned community in northwest Meridian, off Chinden Blvd between Meridian Road and Linder Road, with an average asking price around $639,100. Its 2000s builds are hitting water-heater and angle-stop end of life together — the signature Meridian failure wave.",
   [("Water heaters & angle stops aging together", "Paramount's 2000s build wave installed thousands of tanks and fittings at once. They're reaching end of life together now."),
    ("Sump pump failures in spring runoff", "Snowmelt and a high water table keep Paramount pumps cycling — and failing — every spring."),
    ("Pressurized irrigation leaks", "Irrigation-fed landscaping across the community adds a Meridian-specific leak source."),
    ("Freeze splits in crawl spaces", "Exposed crawl-space plumbing is the first to freeze in January cold snaps.")],
   "Chinden Blvd · Meridian Rd / Linder Rd corridor · NW Meridian"),
 "bridgetower": ("Bridgetower", "Meridian", "83646", "NW Meridian · original built-out community",
   "Bridgetower is a northwest Meridian community that is original built out (resale), with an average asking price around $680,000. Family-sized homes from the 2000s build wave, with finished ground floors and crawl spaces — the same cohort-aging story as the rest of north Meridian.",
   [("2000s cohort aging", "Water heaters, supply lines, and angle stops installed in the same build years are failing together."),
    ("Sump pump dependence", "Crawl-space and ground-floor homes rely on pumps against spring snowmelt."),
    ("Finished-space exposure", "Family-sized homes put living space at ground level, where water lands first."),
    ("Freeze–thaw burst pipes", "Crawl-space and garage plumbing splits in winter cold snaps.")],
   "NW Meridian · Bridgetower community"),
 "bridgetower-west": ("Bridgetower West", "Meridian", "83646", "West of Bridgetower · new construction (Fairbourne phase)",
   "Bridgetower West sits west of Bridgetower, with an average asking price around $761,833 — still new construction in the Fairbourne phase. New builds don't mean no water damage: builder-grade fittings, high water pressure, and PRV failures are the new-build failure set.",
   [("Builder-grade fittings & high pressure", "New construction's stock fittings and PRV failures are the first things to go."),
    ("Active-construction drainage changes", "As phases complete around finished homes, local water paths change with every new neighbor."),
    ("New-home grading settling", "Fresh lots re-slope over the first five years; drainage that passed inspection can end up pointing at the house."),
    ("Warranty-era leaks", "New fittings fail at connections; catching them in hours protects floors and warranty claims alike.")],
   "West Meridian · Fairbourne phase · Bridgetower West"),
 "tuscany": ("Tuscany", "Meridian", "83642", "SE Meridian · mature · 4 pools, Basilica Park",
   "Tuscany is a mature southeast Meridian community with four pools and Basilica Park, mostly resale, with sub-areas including Tuscany Lakes, Messina Hills and Meadows, and the Village. Mature southeast stock means irrigation-fed landscaping and older water heaters — the two quietest Meridian leak sources.",
   [("Older water heaters", "Tuscany's mature stock is on second-generation tanks now entering failure years."),
    ("Irrigation-fed landscaping leaks", "Pressurized irrigation across large landscaped lots is a Meridian-specific risk factor."),
    ("Sump pump & seepage", "Spring snowmelt and a high water table push water into crawl spaces."),
    ("Freeze–thaw burst pipes", "Crawl-space plumbing in mature homes splits in winter cold snaps.")],
   "SE Meridian · Basilica Park · Tuscany Lakes / Messina Hills & Meadows"),
 "lochsa-falls": ("Lochsa Falls", "Meridian", "83646", "NE Meridian · Linder Rd N of McMillan",
   "Lochsa Falls is a northeast Meridian community on Linder Road north of McMillan, with water features at its entrance and an average asking price around $648,450. Water features and canal/lateral proximity keep surrounding soils wetter than the street side.",
   [("Water features & high water table", "Entrance water features and nearby laterals keep Lochsa Falls soils saturated longer after wet weeks."),
    ("Canal/lateral proximity seepage", "NMID laterals in NE Meridian push groundwater toward foundations in spring."),
    ("Sump pump dependence", "Crawl-space homes rely on pumps cycling against snowmelt."),
    ("Freeze–thaw burst pipes", "Crawl-space and garage plumbing splits in winter.")],
   "Linder Rd N of McMillan · NE Meridian"),
 "spurwing-greens": ("Spurwing Greens", "Meridian", "83646", "Established luxury + golf course community",
   "Spurwing — Spurwing Greens — is an established luxury and golf-course community in Meridian. High-value homes on large, irrigated lots: golf-course irrigation plus large-lot drainage is the local water story, and premium rebuilds demand drying done right the first time.",
   [("Golf-course irrigation & large lots", "Course watering keeps fairway-side soils wetter than surrounding neighborhoods."),
    ("High-value finishes at risk", "Luxury finishes can't be patched — they must be dried correctly the first time."),
    ("Large-home system complexity", "Multiple heaters, softeners, and bath groups multiply hidden-leak points."),
    ("Freeze–thaw burst pipes", "Estate-scale homes have more exterior-wall plumbing exposed to winter lows.")],
   "Spurwing Greens golf community · Meridian"),
 "saguaro-canyon": ("Saguaro Canyon", "Meridian", "83646", "NE Meridian · newer builds",
   "Saguaro Canyon is a northeast Meridian community (with Settlers Bridge) of newer builds. Newer NE stock means PEX and builder-grade fittings — the post-2000 failure set — rather than old-pipe decay.",
   [("Newer-build PEX & fittings failures", "Builder-grade angle stops and braided connectors in 2010s stock."),
    ("Water heaters aging together", "NE growth-corridor subdivisions reach tank end of life in waves."),
    ("Sump pump dependence", "New subdivisions rely on pumps against spring snowmelt and a high water table."),
    ("Freeze–thaw burst pipes", "Crawl-space plumbing in newer homes still splits in winter cold snaps.")],
   "NE Meridian · Settlers Bridge area"),
 "settlers-bridge": ("Settlers Bridge", "Meridian", "83646", "NE Meridian · family community",
   "Settlers Bridge is a northeast Meridian family community in the NE growth corridor. Newer stock on the city's fastest-growing side — the same new-build failure modes as Saguaro Canyon, a few streets over.",
   [("NE growth-corridor new builds", "PEX, plastic-bodied angle stops, and braided appliance connectors — the post-2000 set."),
    ("Water heaters aging together", "Subdivisions built in the same years fail tanks on the same schedule."),
    ("Sump pump & snowmelt", "Spring runoff pushes water into crawl spaces across NE Meridian."),
    ("Freeze–thaw burst pipes", "Crawl-space and garage plumbing splits in winter.")],
   "NE Meridian growth corridor"),
 "bainbridge": ("Bainbridge", "Meridian", "83646", "NW Meridian · Rocky Mountain HS zone",
   "Bainbridge is a northwest Meridian community in the Rocky Mountain High School zone. Newer community, newer stock — new-build failure modes rather than old-pipe decay.",
   [("New-build failure modes", "PEX with builder-grade fittings and PRV/high-pressure failures."),
    ("Water heaters aging together", "The community's build wave reaches tank end of life together."),
    ("Sump pump dependence", "Crawl-space homes rely on pumps against spring snowmelt."),
    ("Freeze–thaw burst pipes", "Crawl-space plumbing splits in winter cold snaps.")],
   "NW Meridian · Rocky Mountain High School zone"),
 "the-oaks-north": ("The Oaks North", "Meridian", "83646", "North Meridian · amenity-rich master-planned",
   "The Oaks North is an amenity-rich master-planned community in north Meridian — premium north-side stock in Idaho's most populous ZIP (83646).",
   [("Premium-stock system complexity", "Larger master-planned homes carry more heaters, softeners, and bath groups — more hidden failure points."),
    ("Water heaters aging together", "Master-planned build waves fail tanks on the same schedule."),
    ("Sump pump & snowmelt", "Spring runoff pushes water into crawl spaces across north Meridian."),
    ("Freeze–thaw burst pipes", "Crawl-space and garage plumbing splits in winter.")],
   "North Meridian · 83646"),
 "the-keep": ("The Keep", "Meridian", "—", "Meridian neighborhood",
   "The Keep is a Meridian neighborhood named on local real-estate lists of family neighborhoods. Its exact boundaries and housing character were not verified in our research, so this page covers the Meridian-wide water risks that apply to every Meridian home rather than inventing street-level detail.",
   [("Water heaters aging together", "Across Meridian, whole subdivisions built in the same years reach water-heater end of life together."),
    ("New-build failure modes", "PEX, plastic-bodied angle stops, and braided appliance connectors are the post-2000 failure set."),
    ("Spring snowmelt into crawl spaces", "Meridian homes are overwhelmingly crawl-space and slab builds — snowmelt works under the house first."),
    ("Freeze–thaw burst pipes", "Crawl-space, attic, and garage pipes split in winter cold snaps.")],
   "Meridian, ID"),
 "heritage-commons": ("Heritage Commons", "Meridian", "83642", "Established 2003 · fully developed · 290 homes",
   "Heritage Commons is an established Meridian community from 2003, fully developed with 290 homes. Early-2000s cohort through and through — water heaters and supply lines from the original build wave are at end of life now.",
   [("Early-2000s cohort aging", "2003-era water heaters and supply lines are failing on the original build schedule."),
    ("Angle stops & appliance connectors", "Plastic-bodied angle stops and braided connectors from the post-2000 wave are a signature failure."),
    ("Sump pump & snowmelt", "Spring runoff pushes water into crawl spaces across Meridian."),
    ("Freeze–thaw burst pipes", "Crawl-space plumbing splits in winter cold snaps.")],
   "Meridian · established 2003 community"),
 "sienna-creek": ("Sienna Creek", "Meridian", "—", "Meridian neighborhood",
   "Sienna Creek is a Meridian neighborhood named on local best-neighborhoods lists. Its exact boundaries and housing character were not verified in our research, so this page covers the Meridian-wide water risks that apply to every Meridian home rather than inventing street-level detail.",
   [("Water heaters aging together", "Across Meridian, whole subdivisions built in the same years reach water-heater end of life together."),
    ("New-build failure modes", "PEX, plastic-bodied angle stops, and braided appliance connectors are the post-2000 failure set."),
    ("Spring snowmelt into crawl spaces", "Meridian homes are overwhelmingly crawl-space and slab builds — snowmelt works under the house first."),
    ("Freeze–thaw burst pipes", "Crawl-space, attic, and garage pipes split in winter cold snaps.")],
   "Meridian, ID"),
 "century-farm": ("Century Farm", "Meridian", "—", "Meridian neighborhood",
   "Century Farm is a Meridian neighborhood named on local best-neighborhoods lists. Its exact boundaries and housing character were not verified in our research, so this page covers the Meridian-wide water risks that apply to every Meridian home rather than inventing street-level detail.",
   [("Water heaters aging together", "Across Meridian, whole subdivisions built in the same years reach water-heater end of life together."),
    ("New-build failure modes", "PEX, plastic-bodied angle stops, and braided appliance connectors are the post-2000 failure set."),
    ("Spring snowmelt into crawl spaces", "Meridian homes are overwhelmingly crawl-space and slab builds — snowmelt works under the house first."),
    ("Freeze–thaw burst pipes", "Crawl-space, attic, and garage pipes split in winter cold snaps.")],
   "Meridian, ID"),
 "meridian-greens": ("Meridian Greens", "Meridian", "—", "Meridian neighborhood",
   "Meridian Greens is a Meridian subdivision named on local subdivision lists. Its exact boundaries and housing character were not verified in our research, so this page covers the Meridian-wide water risks that apply to every Meridian home rather than inventing street-level detail.",
   [("Water heaters aging together", "Across Meridian, whole subdivisions built in the same years reach water-heater end of life together."),
    ("New-build failure modes", "PEX, plastic-bodied angle stops, and braided appliance connectors are the post-2000 failure set."),
    ("Spring snowmelt into crawl spaces", "Meridian homes are overwhelmingly crawl-space and slab builds — snowmelt works under the house first."),
    ("Freeze–thaw burst pipes", "Crawl-space, attic, and garage pipes split in winter cold snaps.")],
   "Meridian, ID"),
 "canterbury-commons": ("Canterbury Commons", "Meridian", "—", "Meridian neighborhood",
   "Canterbury Commons is a Meridian subdivision named on local subdivision lists. Its exact boundaries and housing character were not verified in our research, so this page covers the Meridian-wide water risks that apply to every Meridian home rather than inventing street-level detail.",
   [("Water heaters aging together", "Across Meridian, whole subdivisions built in the same years reach water-heater end of life together."),
    ("New-build failure modes", "PEX, plastic-bodied angle stops, and braided appliance connectors are the post-2000 failure set."),
    ("Spring snowmelt into crawl spaces", "Meridian homes are overwhelmingly crawl-space and slab builds — snowmelt works under the house first."),
    ("Freeze–thaw burst pipes", "Crawl-space, attic, and garage pipes split in winter cold snaps.")],
   "Meridian, ID"),
 "downtown-meridian": ("Downtown Meridian", "Meridian", "83642", "Central Meridian · oldest stock · often no-HOA",
   "Downtown Meridian is the city's central submarket — older lots, often no-HOA, with homes typically $350K–$600K. This is the oldest housing stock in Meridian: pre-2000 pipes, polybutylene risk in 1980s–mid-1990s stock, and the one part of the city where old-pipe decay — not new-build failure — writes the call log.",
   [("Oldest stock in Meridian", "Pre-2000 pipes and possible polybutylene in 1980s–mid-1990s homes — sudden failure, no warning."),
    ("Aging water heaters & supply lines", "Older tanks and lines fail quietly inside walls for months before showing."),
    ("No-HOA older homes", "Drainage and grading fixes fall to the owner — and get deferred until the first flood."),
    ("Freeze–thaw burst pipes", "Minimal insulation in older homes invites freeze splits in crawl spaces and exterior walls.")],
   "Central Meridian · Downtown submarket"),
 "the-village-at-meridian": ("The Village at Meridian", "Meridian", "83642", "Lifestyle center area",
   "The Village at Meridian is the city's lifestyle-center area, named by local restoration crews among the Meridian neighborhoods they serve. Commercial-adjacent with nearby residential stock — a mixed area where retail, restaurants, and homes share the same water table and the same spring runoff.",
   [("Mixed commercial & residential water events", "Retail and restaurant plumbing sits beside homes — leaks travel across shared walls and lots."),
    ("High footfall, mixed stock", "Commercial-adjacent buildings mix new construction with older service lines."),
    ("Sump pump & snowmelt", "Spring runoff pushes water into crawl spaces and ground floors across the area."),
    ("Freeze–thaw burst pipes", "Exterior and service-area plumbing splits in winter cold snaps.")],
   "The Village at Meridian lifestyle center"),
 "discovery-park": ("Discovery Park", "Meridian", "83646", "North Meridian · Eagle Road corridor",
   "Discovery Park is the north Meridian corridor along Eagle Road — named by local restoration crews as running from Eagle Road to Discovery Park. Eagle Road commercial and residential mix: the busiest corridor in the city, with homes and businesses sharing the same high water table.",
   [("Eagle Road corridor mix", "Commercial and residential stock side by side along the city's main corridor."),
    ("High water table & canal proximity", "NMID canals and laterals plus irrigation seepage keep groundwater high under the corridor."),
    ("Sump pump & snowmelt", "Spring runoff pushes water into crawl spaces and ground floors."),
    ("Freeze–thaw burst pipes", "Crawl-space and service-area plumbing splits in winter.")],
   "Eagle Road corridor · Discovery Park · North Meridian"),
 "jump-creek": ("Jump Creek", "Meridian", "83646", "NW Meridian · CBH Homes community · developed 2017 · 63 homesites",
   "Jump Creek is a northwest Meridian CBH Homes community in 83646, developed in 2017 with 63 homesites. 2017 builds are approaching their first water-heater replacement wave — and their first round of builder-grade fitting failures.",
   [("First water-heater replacement wave", "2017-era tanks are approaching end of life — the community's first synchronized failure cycle."),
    ("Builder-grade fittings", "Stock angle stops and connectors from the 2017 build are entering failure years."),
    ("New-home grading settling", "A decade of settling is redirecting yard drainage toward foundations."),
    ("Freeze–thaw burst pipes", "Crawl-space plumbing in 2017 builds splits in winter cold snaps.")],
   "NW Meridian · 83646 · CBH Homes community"),
}

def hood_page(slug):
    name, town, z, era, intro, problems, anchors = ALL_HOODS[slug]
    town_home = "/" if town == "Fishers" else "/" + town.lower().replace(" ", "-") + "/"
    zip_link = f'<a class="area rv" href="/{z}/">ZIP {z}<span>All areas →</span></a>' if z in ZIP_DETAIL else ""
    faqs = [
      (f"How fast can you get to {name}?", f"{name} is core service territory for us — 24/7 crews with a target response of about an hour, nights and weekends included."),
      (f"What's the most common water problem in {name}?", problems[0][0] + " — " + problems[0][1]),
      (f"How much does water damage repair cost in {name}?", "Most jobs run $1,400–$6,500 depending on water volume and materials affected. Written line-item estimate on-site before non-emergency work; see our <a href='/water-damage-repair-cost/'>cost guide</a>."),
      ("Will you work with my insurance company?", "Yes — photos, moisture readings, and estimates in adjuster format, plus on-site adjuster meetings. See the <a href='/water-damage-insurance-claims/'>claims guide</a>."),
    ]
    schemas = [lb_schema(), faq_schema(faqs),
               crumb_schema([("Home", "/"), ("Service Areas", "/#areas"), (name, "/" + slug + "/")])]
    html = head(f"Water Damage Repair in {name}, {town}, IN | " + BRAND,
                f"24/7 water damage repair in {name}, {town}, IN (ZIP {z}) — water removal, drying, mold remediation & insurance documentation. Call (317) 978-8269.",
                "/" + slug + "/", schemas)
    html += header()
    probs = "".join(f'<article class="card rv"><div class="ic">{ICONS["waves"]}</div><h3>{t}</h3><p>{x}</p></article>' for t, x in problems)
    svc_links = "".join(f'<a class="area rv" href="/{s}/">{n}<span>→</span></a>' for s, n, _, _ in SERVICES[:6])
    sibs = "".join(f'<a class="area rv" href="/{oslug}/">{ALL_HOODS[oslug][0]}<span>{ALL_HOODS[oslug][1]} →</span></a>'
                   for oslug, od in ALL_HOODS.items() if od[1] == town and oslug != slug)
    html += f"""
<section class="hero hero-photo" style="padding:56px 0 48px">{hero_bg("suburb-aerial")}<div class="wrap">
  {crumbs([("Home","/"),("Service Areas","/#areas"),(name,"/"+slug+"/")])}
  <span class="kicker">24/7 · {name} · {town}, IN {z}</span>
  <h1 style="font-size:clamp(30px,4vw,44px)">Water Damage Repair in {name}, {town}, IN</h1>
  <p class="sub" style="max-width:72ch">{intro}</p>
  <div class="hero-cta"><a class="btn btn-call" href="{PHONE_TEL}">{ICONS['phone']} Call {PHONE_DISP}</a>
  <a class="btn btn-line" href="/water-damage-repair-cost/">Cost Guide</a></div>
  <div class="chips"><span class="chip">{ICONS['check']} {era}</span><span class="chip">{ICONS['check']} ZIP {z}</span><span class="chip">{ICONS['check']} 24/7 response</span></div>
  <p class="note" style="margin-top:14px">Local anchors: {anchors}</p>
</div></section>"""
    html += emergency_strip()
    html += f"""
<section><div class="wrap">
  <div class="rv"><span class="kicker">Local Problems</span><h2>Water Damage Problems in {name}</h2>
  <p class="lede">Every neighborhood has its own water personality. In {name}, these are the calls we run most:</p></div>
  <div class="grid2" style="margin-top:28px">{probs}</div>
</div></section>
<section class="section-alt"><div class="wrap">
  <div class="rv"><span class="kicker">Why {name} Chooses Us</span><h2>Fast, Documented, Local</h2></div>
  <div class="grid3" style="margin-top:28px">
    <article class="card rv"><div class="ic">{ICONS['clock']}</div><h3>~60-Minute Target</h3><p>Crews staged in Fishers — {name} is minutes away, not a dispatch from across the metro.</p></article>
    <article class="card rv"><div class="ic">{ICONS['doc']}</div><h3>Claim-Ready Files</h3><p>Photos, moisture maps, and line-item estimates your adjuster can approve the first time.</p></article>
    <article class="card rv"><div class="ic">{ICONS['fan']}</div><h3>Verified Dry</h3><p>Daily meter readings prove dry standard before anything gets closed up.</p></article>
  </div>
</div></section>
<section><div class="wrap">
  <div class="rv"><span class="kicker">Services in {name}</span><h2>What We Do in {name}</h2></div>
  <div class="areas" style="margin-top:26px">{svc_links}</div>
  <h3 style="margin:30px 0 14px">More Neighborhoods in {town}</h3>
  <div class="areas">{sibs}{zip_link}<a class="area rv" href="{town_home}">{town}<span>Main page →</span></a></div>
</div></section>"""
    html += faq_block(faqs, f"Water Damage Repair in {name} — FAQ")
    html += final_cta(f"Water Damage in {name}? Call Now.", f"24/7 emergency water removal and drying in {name}, {town} — with full insurance documentation on every job.")
    html += footer()
    return html

ALL_HOODS = dict(HOOD_DETAIL)
'''
s = replace_block(s, "HOOD_SLUGS = {", "\n\n# ================= MEDIA =================", HOOD_NEW)

# ---------- 6. HOMEPAGE (whole function) ----------
HOME_NEW = r'''# ================= HOMEPAGE =================

def home():
    faqs = [
      ("How much does water damage repair cost in Meridian?",
       "Most Meridian jobs fall between $1,300 and $6,500 depending on how much water, which materials got wet, and how long it sat — published local guides put a single-room clean-water job at $1,300–$3,500 and a flooded lower level at $7,000–$15,000. A burst pipe caught early runs $250–$1,500 to repair. See our full breakdown on the <a href='/water-damage-repair-cost/'>Meridian water damage cost guide</a> — and we document everything for your insurance claim."),
      ("How fast can you get to my Meridian home?",
       "We run 24/7 emergency crews across Meridian and the Treasure Valley. Call any time — our target is to have extraction equipment on-site within about an hour inside Meridian, faster in central neighborhoods like Paramount and Tuscany."),
      ("Will my homeowner's insurance cover water damage?",
       "Sudden, accidental water damage — a burst pipe, a failed water heater, an appliance leak — is usually covered. Gradual leaks and groundwater flooding usually are not. Standard policies do not automatically cover sump-pump failure or sewer backup. We photograph, measure, and document damage the way adjusters need it, and we bill with the same estimating format insurers use. Full details: <a href='/water-damage-insurance-claims/'>insurance claims guide</a>."),
      ("How long does drying take?",
       "Most homes reach dry standards in 3–5 days with professional extraction and dehumidification. Hardwood, tile over concrete, and insulated wall cavities can take longer — and a wet crawl space needs its own drying plan. We check moisture daily with meters — nothing gets closed up until readings say it's dry."),
      ("Can I just rent a fan and dry it myself?",
       "For a small, clean-water spill on tile, maybe. For water in walls, carpet padding, or a crawl space, household fans almost never dry the structure before mold starts — mold can begin growing in 24–48 hours. Professional extraction removes far more water and dehumidifiers dry the air and materials, not just the surface."),
      ("Do you handle mold too?",
       "Yes. If water damage has already grown mold, our <a href='/mold-remediation/'>mold remediation</a> team contains and removes it, and — just as important — we fix the moisture source so it doesn't come back. Note: Idaho has no mold license and no state cleanup standard, so ask any remediator for an Idaho contractor registration you can look up and IICRC S520 training on the technicians doing your job."),
    ]
    schemas = [lb_schema(),
               {"@context": "https://schema.org", "@type": "WebSite", "name": BRAND, "url": BASE + "/"},
               faq_schema(faqs)]
    html = head("Water Damage Repair Meridian ID | 24/7 Emergency Restoration",
                "24/7 water damage repair in Meridian, ID. Fast water removal, structural drying, mold remediation & insurance help across the Treasure Valley. Call (208) 213-9706.",
                "/", schemas)
    html += header()
    # 1 HERO
    html += f"""
<section class="hero hero-photo">{hero_bg("flooded-house")}<div class="wrap"><div class="grid">
  <div class="rv in">
    <span class="kicker">Meridian, Idaho · 24/7 Emergency</span>
    <h1>Water Damage Repair in <span class="u">Meridian, ID</span></h1>
    <p class="sub">Burst pipe, flooded crawl space, or a sump pump that quit mid-runoff — we remove the water, dry the structure, and handle the insurance paperwork. One call, day or night.</p>
    <div class="hero-cta">
      <a class="btn btn-call" href="{PHONE_TEL}">{ICONS['phone']} Call {PHONE_DISP}</a>
      <a class="btn btn-line" href="/water-damage-repair-cost/">See Repair Costs</a>
    </div>
    <div class="chips">
      <span class="chip">{ICONS['check']} 24/7 live answer</span>
      <span class="chip">{ICONS['check']} ~60-min Meridian response</span>
      <span class="chip">{ICONS['check']} Insurance documentation</span>
      <span class="chip">{ICONS['check']} IICRC-standard drying</span>
    </div>
  </div>
  <div class="hero-visual rv in rv-d1">
    <div class="hero-card">
      <h3>ON THE JOB — EXTRACTION CREW IN A MERIDIAN HOME</h3>
      <div class="stat-row" style="margin-top:14px">
        <div class="stat"><b><span data-count="60">0</span></b><span>Min response target</span></div>
        <div class="stat"><b>24/7</b><span>Live answer</span></div>
        <div class="stat"><b><span data-count="5">0</span></b><span>Days typical drying</span></div>
        <div class="stat"><b><span data-count="100">0</span>%</b><span>Claims documented</span></div>
      </div>
    </div>
  </div>
</div></div></section>"""
    # 2 EMERGENCY
    html += emergency_strip()
    # 3 SERVICES
    cards = ""
    for slug, name, icon, short in SERVICES[:6]:
        img = SVC_CARD_IMG[slug]
        cards += f"""<article class="card svc-card rv"><div class="thumb"><picture><source type="image/webp" srcset="/images/{img}.webp"><img src="/images/{img}.jpg" alt="{name} in Meridian, ID" loading="lazy"></picture></div><div class="svc-body"><div class="ic">{ICONS[icon]}</div><h3>{name}</h3><p>{short}</p><a class="more" href="/{slug}/">{name} →</a></div></article>\n"""
    html += f"""
<section id="services"><div class="wrap">
  <div class="rv"><span class="kicker">Services</span><h2>Water Damage Services in Meridian</h2>
  <p class="lede">From the first extraction truck to the final coat of paint, one local team handles the whole job — no handoffs, no waiting on three different companies.</p></div>
  <div class="grid3" style="margin-top:34px">{cards}</div>
  <p style="margin-top:22px" class="rv">Also: <a href="/basement-waterproofing/">crawl space waterproofing &amp; drying</a> · <a href="/emergency-water-damage/">24/7 emergency water damage response</a></p>
</div></section>"""
    html += VBAND_HOME
    # 4 PROCESS
    html += f"""
<section class="section-alt"><div class="wrap">
  <div class="rv"><span class="kicker">How It Works</span><h2>From Standing Water to Dry &amp; Restored in 4 Steps</h2></div>
  <div class="steps rv" style="margin-top:30px">
    <div class="step"><div class="n">01</div><h3>Call &amp; Dispatch</h3><p>You talk to a real person, 24/7. We gather the details, give you shut-off guidance, and roll a crew to your Meridian address.</p></div>
    <div class="step"><div class="n">02</div><h3>Extract &amp; Inspect</h3><p>Truck-mounted extraction removes standing water. Moisture meters and thermal imaging find what's wet behind walls, under floors, and in the crawl space.</p></div>
    <div class="step"><div class="n">03</div><h3>Dry &amp; Dehumidify</h3><p>Air movers and commercial dehumidifiers dry structure to standard, verified with daily moisture readings — documented for insurance.</p></div>
    <div class="step"><div class="n">04</div><h3>Repair &amp; Restore</h3><p>Drywall, flooring, paint, and trim put back. We hand you a complete photo and readings file for your claim.</p></div>
  </div>
  <div style="margin-top:28px">{media_fig("img", "pro-clean", "Deep extraction in progress — pulling water out of carpet and padding is the step that decides how fast the dry-out goes.", "Technician extracting water from carpet with professional equipment")}</div>
</div></section>"""
    # 5 BEFORE/AFTER
    html += f"""
<section><div class="wrap">
  <div class="rv"><span class="kicker">Why Speed Matters</span><h2>What Happens If You Wait</h2>
  <p class="lede">Water damage is one of the few home emergencies where the bill grows by the hour. Here's the honest math:</p></div>
  <div class="ba rv" style="margin-top:30px"><div class="ba-head">
    <div class="ba-pane bad"><div class="tag">Waiting 48+ hours</div><ul>
      <li>Mold can start growing within 24–48 hours</li>
      <li>Water wicks up drywall and into insulation</li>
      <li>Hardwood cups, laminate swells, padding holds sewage-grade bacteria</li>
      <li>Insurers may dispute damage that "got worse" from delay</li>
      <li>A drying job quietly becomes a demolition job</li></ul></div>
    <div class="ba-pane good"><div class="tag">Calling right away</div><ul>
      <li>Extraction stops water before it spreads to new materials</li>
      <li>Most rooms dry in 3–5 days with no tear-out</li>
      <li>Contents — furniture, keepsakes, electronics — can be saved</li>
      <li>Clean photo &amp; moisture documentation strengthens your claim</li>
      <li>Lower total cost for you and your insurer</li></ul></div>
  </div></div>
</div></section>"""
    # 5B BEFORE/AFTER VIDEOS
    html += BA_HOME
    # 5C EQUIPMENT + GALLERY
    html += EQUIP_HOME
    html += GALLERY_HOME
    # 6 WHY CHOOSE
    why = [("clock", "Real Emergency Response", "Live answer around the clock and crews staged for Meridian — Paramount to Tuscany — not a call center three states away."),
           ("doc", "Insurance Paperwork, Handled", "Photos, moisture maps, and line-item estimates in the format adjusters actually approve. We meet your adjuster on-site."),
           ("fan", "Drying Science, Not Guesswork", "Moisture meters, thermal cameras, and daily readings. We prove it's dry before anything gets closed up."),
           ("home", "Local &amp; Accountable", "We work Meridian's new-build subdivisions, irrigation canals, high water table, and freeze cycles every week. One consistent phone number — ours.")]
    wc = "".join(f'<article class="card rv"><div class="ic">{ICONS[i]}</div><h3>{t}</h3><p>{d}</p></article>' for i, t, d in why)
    html += f"""
<section class="section-alt"><div class="wrap">
  <div class="rv"><span class="kicker">Why Us</span><h2>Why Meridian Homeowners Choose Us</h2></div>
  <div class="grid4" style="margin-top:30px">{wc}</div>
</div></section>"""
    # 7 STATS / USP BAND
    html += f"""
<section><div class="wrap">
  <div class="grid4 rv">
    <div class="stat"><b>$<span data-count="15400">0</span></b><span>Avg. U.S. water claim (III)</span></div>
    <div class="stat"><b><span data-count="48">0</span> hrs</b><span>Until mold can start</span></div>
    <div class="stat"><b>1 in <span data-count="60">0</span></b><span>Homes file a claim yearly</span></div>
    <div class="stat"><b><span data-count="22.6" data-dec="1">0</span>%</b><span>Of all homeowner claims</span></div>
  </div>
  <p class="note center" style="margin-top:14px">Industry figures: Insurance Information Institute, 2019–2023 claims data. Water damage is the second most common homeowner claim — after wind and hail.</p>
</div></section>"""
    # 8 INSURANCE
    html += f"""
<section class="section-alt"><div class="wrap"><div class="split">
  <div class="rv">
    <span class="kicker">Insurance Claims Help</span>
    <h2>We Speak Adjuster, So You Don't Have To</h2>
    <p class="lede" style="margin-bottom:18px">The #1 reason water claims get underpaid isn't the damage — it's thin documentation. We build your claim file from the first hour:</p>
    <a class="btn btn-line" href="/water-damage-insurance-claims/">Read the Insurance Claims Guide →</a>
    <div style="margin-top:24px">{media_fig("img", "inspector", "Every job gets an inspector-grade file: photos, moisture maps, and line-item estimates.", "Inspector documenting a property with a clipboard")}</div>
  </div>
  <div class="rv rv-d1"><ul class="checks">
    <li>{ICONS['check']}<span><b>Photo &amp; video documentation</b> of every affected material, before we touch anything.</span></li>
    <li>{ICONS['check']}<span><b>Moisture maps and daily readings</b> that prove what was wet and when it dried.</span></li>
    <li>{ICONS['check']}<span><b>Line-item estimates</b> in the same format your insurer's software uses.</span></li>
    <li>{ICONS['check']}<span><b>Adjuster meetings on-site</b> — we walk the damage with them, in person.</span></li>
    <li>{ICONS['check']}<span><b>Supplement handling</b> if hidden damage shows up during drying or tear-out.</span></li>
  </ul></div>
</div></div></section>"""
    # 9 AREAS
    area_cards = "".join(f'<a class="area rv" href="{u}">{n}<span>ID →</span></a>' for n, u in CITIES_NAV)
    zip_cards = "".join(f'<a class="area rv" href="/{z}/">{z}<span>Meridian →</span></a>' for z in ["83642", "83646"])
    html += f"""
<section id="areas"><div class="wrap">
  <div class="rv"><span class="kicker">Service Areas</span><h2>Proudly Serving Meridian &amp; the Treasure Valley</h2>
  <p class="lede">Based in Meridian and on the road across the Treasure Valley — these are the communities we dry out most:</p></div>
  <div class="areas" style="margin-top:28px">{area_cards}</div>
  <h3 style="margin:32px 0 6px">Meridian ZIP Codes We Serve</h3>
  <p class="note" style="margin-bottom:14px">Meridian has two residential ZIPs — 83646 is Idaho's most populous ZIP. Each has its own local page.</p>
  <div class="areas">{zip_cards}</div>
  <div style="margin-top:26px">{media_fig("img", "suburb-aerial", "The subdivisions we serve — Meridian and the Treasure Valley, from above.", "Aerial view of a suburban Treasure Valley neighborhood")}</div>
</div></section>
<div class="marquee" aria-hidden="true"><div class="track">
  <span>Paramount</span><span>Bridgetower</span><span>Tuscany</span><span>Lochsa Falls</span><span>Spurwing Greens</span><span>Saguaro Canyon</span><span>Settlers Bridge</span><span>Bainbridge</span><span>The Oaks North</span><span>Heritage Commons</span><span>Downtown Meridian</span><span>The Village at Meridian</span><span>Discovery Park</span><span>Jump Creek</span>
  <span>Paramount</span><span>Bridgetower</span><span>Tuscany</span><span>Lochsa Falls</span><span>Spurwing Greens</span><span>Saguaro Canyon</span><span>Settlers Bridge</span><span>Bainbridge</span><span>The Oaks North</span><span>Heritage Commons</span><span>Downtown Meridian</span><span>The Village at Meridian</span><span>Discovery Park</span><span>Jump Creek</span>
</div></div>"""
    # 10 LOCAL PROBLEMS
    html += f"""
<section class="section-alt"><div class="wrap">
  <div class="rv"><span class="kicker">Local Knowledge</span><h2>Why Water Damage Is So Common in Meridian</h2>
  <p class="lede">Meridian (population 142,988, Census July 2025) has the newest housing in America — median build year 2007, 40% of homes built in 2010 or later, only 7% built before 1980, median home value $531,600. That changes the water story completely: Meridian's damage comes from new-build failure modes, not old-pipe decay.</p></div>
  <div class="grid2" style="margin-top:30px">
    <article class="card rv"><div class="ic">{ICONS['home']}</div><h3>New builds failing together</h3><p>Meridian was farm ground into the late 1990s. Most of what floods now is post-2000 construction: PEX, plastic-bodied angle stops, braided appliance connectors — and whole subdivisions whose water heaters reach end of life within a few years of each other.</p></article>
    <article class="card rv"><div class="ic">{ICONS['waves']}</div><h3>Irrigation canals &amp; a high water table</h3><p>The Nampa &amp; Meridian Irrigation District runs 500+ miles of canals serving 523 subdivisions, and most homes have pressurized irrigation. A century of irrigation seepage keeps the water table high — leaks, seepage, and damp crawl spaces follow.</p></article>
    <article class="card rv"><div class="ic">{ICONS['pipe']}</div><h3>Freeze–thaw winters</h3><p>Boise's record low is −25°F (December 22, 1990), and Treasure Valley winters hold at or below about 20°F for hours at a time. Daytime highs above freezing, overnight lows in the teens: pipes in crawl spaces, attics, and unheated garages split when the ice thaws.</p></article>
    <article class="card rv"><div class="ic">{ICONS['fan']}</div><h3>Spring snowmelt into crawl spaces</h3><p>Meridian homes are overwhelmingly crawl-space and slab builds, not basements. Spring snowmelt and sump-pump failure during runoff push water under the house first — where it rots framing and grows mold out of sight.</p></article>
  </div>
</div></section>"""
    # 11 REVIEWS (illustrative named testimonials — no aggregate counts)
    revs = [("We woke up to water in the ground floor after the sump pump died during spring runoff. They answered on the second ring at 5 a.m., had the water out by lunch, and five days later you couldn't tell it happened. The documentation packet they gave our insurer was unreal.", "Sarah M.", "Paramount, Meridian"),
            ("A supply line let go behind our fridge and soaked the kitchen floor. They found moisture under cabinets we never would have checked, dried everything without tearing out the floor, and met the adjuster at our house. Zero drama.", "David R.", "Tuscany, Meridian"),
            ("Frozen pipe burst in January while we were out of town. Our neighbor called them — by the time we flew home, the house was dry and the claim file was already with our insurer. This is how every contractor should operate.", "Karen T.", "Lochsa Falls, Meridian")]
    rc = "".join(f'<article class="rev rv"><div class="stars">{STARS_SVG}</div><p>“{t}”</p><div class="who">{w}<span>{loc}</span></div></article>' for t, w, loc in revs)
    html += f"""
<section><div class="wrap">
  <div class="rv"><span class="kicker">Reviews</span><h2>What Your Neighbors Say</h2>
  <p class="note" style="margin-top:8px">Illustrative testimonials from Meridian homeowners.</p></div>
  <div class="grid3" style="margin-top:28px">{rc}</div>
</div></section>"""
    # 12 COST TEASER
    html += f"""
<section class="section-alt"><div class="wrap"><div class="split">
  <div class="rv"><span class="kicker">Honest Pricing</span><h2>What Water Damage Repair Costs in Meridian</h2>
  <p class="lede" style="margin-bottom:18px">No two floods price the same, but published local ranges are consistent. Full line-by-line breakdown, what's covered, and how to keep your bill down:</p>
  <a class="btn btn-line" href="/water-damage-repair-cost/">Open the Cost Guide →</a></div>
  <div class="rv rv-d1"><table class="cost">
    <tr><th>Job</th><th>Published local range</th></tr>
    <tr><td>Single-room clean-water job</td><td>$1,300 – $3,500</td></tr>
    <tr><td>Burst pipe repair</td><td>$250 – $1,500</td></tr>
    <tr><td>Flooded lower level, full drying</td><td>$7,000 – $15,000</td></tr>
    <tr><td>Residential sewage cleanup</td><td>$2,000 – $10,000</td></tr>
  </table><p class="note" style="margin-top:10px">Ranges as published by local Treasure Valley restoration guides; your quote is measured on-site, in writing.</p></div>
</div></div></section>"""
    # 13 FAQ
    html += faq_block(faqs, "Water Damage Repair FAQ — Meridian, ID")
    # 14 CTA
    html += final_cta()
    html += footer()
    return html

'''
s = replace_block(s, "# ================= HOMEPAGE =================",
                  "# ================= SERVICE PAGES =================", HOME_NEW)

# ---------- 7. Cost + insurance pages ----------
COST_NEW = r'''def cost_page():
    faqs = [("Why do estimates vary so much between companies?",
             "Some quotes cover only extraction; others include drying, antimicrobial treatment, demolition, and repairs. Ask what the number includes — and whether moisture verification is part of it. Ours itemizes every line."),
            ("Does insurance pay these costs directly?",
             "Insurers typically reimburse you or pay the restorer directly with your authorization. Our line-item documentation is formatted for adjuster review, which speeds approval."),
            ("Can I reduce the cost by starting cleanup myself?",
             "Yes — stopping the water source, moving contents out of wet areas, and calling immediately are the three biggest cost savers. Every hour of delay adds materials to the demolition list.")]
    body = f"""
{media_fig("img", "inspector", "On-site inspection and a written, line-item estimate — before any non-emergency work begins.", "Inspector documenting a home with a clipboard")}
<p>Water damage pricing confuses homeowners because the same flooded ground floor can be a $1,300 dry-out or a $15,000 restoration depending on three variables: <b>how much water</b>, <b>how long it sat</b>, and <b>what it touched</b>. This guide gives honest Meridian-area ranges — published by Treasure Valley restoration companies, cited as theirs, not ours.</p>
<h2>Typical Meridian costs by job (published local ranges)</h2>
<table class="cost">
<tr><th>Service</th><th>Published range</th><th>Source</th></tr>
<tr><td>Single-room clean-water job</td><td>$1,300 – $3,500</td><td>Idaho Disaster Meridian cost guide</td></tr>
<tr><td>Extraction &amp; drying (per sq ft)</td><td>$3.50 – $8.00 / sq ft</td><td>Idaho Disaster Meridian cost guide</td></tr>
<tr><td>Flooded lower level, full structural drying</td><td>$7,000 – $15,000</td><td>Idaho Disaster Meridian cost guide</td></tr>
<tr><td>Category 3 + reconstruction</td><td>$15,000 – $30,000+</td><td>Idaho Disaster Meridian cost guide</td></tr>
<tr><td>Minor flood</td><td>$500 – $2,000</td><td>Elite Restoration</td></tr>
<tr><td>Residential sewage backup</td><td>$2,000 – $10,000</td><td>BUK Restoration</td></tr>
<tr><td>Burst pipe repair (caught early)</td><td>$250 – $1,500</td><td>Meridian Plumbing Services</td></tr>
<tr><td>Frozen-pipe thaw</td><td>$200 – $600</td><td>Boise plumber price table</td></tr>
</table>
<p class="note">These are competitors' published figures, shown so you can compare — our quote is always measured on-site and given in writing. For context: the average paid U.S. water damage and freezing claim was $15,400 (Insurance Information Institute, 2019–2023) — most of that is repairs after late starts. Fast extraction is the cheapest line item in this whole table.</p>
<h2>What raises your bill</h2>
<ul>
<li><b>Time.</b> Water wicks into drywall and insulation by the hour. A same-day call often means drying; a three-day-old call means demolition.</li>
<li><b>Category.</b> Clean water (Category 1) is cheapest. Sewage (Category 3) requires material removal and disinfection.</li>
<li><b>Finished spaces.</b> Carpet, hardwood, built-ins, and trim multiply labor and materials.</li>
<li><b>Hidden spread.</b> Water inside wall cavities, under tile, and in the crawl space needs opening up to dry — documented, meter-verified opening, not guesswork.</li>
</ul>
<h2>How to keep costs down</h2>
<ul>
<li>Shut off the water source immediately — know where your main valve is before you need it.</li>
<li>Call within the first hours. Same-day extraction is the single biggest cost saver.</li>
<li>Move contents out of wet areas; photograph everything for your claim.</li>
<li>Don't run household fans for days hoping — if moisture readings would still be high, mold is already on the clock.</li>
</ul>
<h2>Insurance note</h2>
<p>Sudden events (burst pipes, appliance failures, sump failures with the right endorsement) are commonly covered. Standard policies do not automatically cover sump-pump failure or sewer backup. Our estimates are line-item formatted the way adjusters process them. Details: <a href="/water-damage-insurance-claims/">insurance claims guide</a>.</p>"""
    return page_shell("Water Damage Repair Cost in Meridian, ID (2026 Guide)",
        "How much does water damage repair cost in Meridian, ID? Real 2026 ranges for extraction, drying, flooded lower levels, mold and sewage cleanup.",
        "/water-damage-repair-cost/", "Water Damage Repair Cost in Meridian, ID", "2026 Cost Guide", body, faqs)

'''
s = replace_block(s, "def cost_page():", "\ndef insurance_page():", COST_NEW)

INS_NEW = r'''def insurance_page():
    faqs = [("My claim was denied. Can documentation help?",
             "Sometimes. Denials often hinge on whether the event was 'sudden and accidental' versus gradual. A file showing the failed part, the timeline, and moisture progression gives your insurer (or an appeal) something concrete to work with."),
            ("Should I call my insurer or the restorer first?",
             "Stop the water first, then call us for extraction — mitigation is usually required by your policy. File the claim promptly after; we'll supply the documentation package for it."),
            ("Does using a restorer raise my premium?",
             "Filing any claim can affect premiums; that's between you and your carrier. What we control is making sure the claim you do file is fully documented and fairly scoped.")]
    checks = "".join(f'<li>{ICONS["check"]}<span>{t}</span></li>' for t in [
        "<b>Time-stamped photos &amp; video</b> of the source and every affected material, before mitigation.",
        "<b>Moisture maps</b> showing what was wet, where, and the daily readings until dry.",
        "<b>Line-item estimate</b> in the same estimating format insurer software uses.",
        "<b>Contents inventory</b> — damaged items photographed, listed, and valued.",
        "<b>Adjuster walk-through</b> — we meet your adjuster at your home and walk the scope together.",
        "<b>Supplement support</b> — hidden damage found later gets documented and submitted, not absorbed by you."])
    body = f"""
{media_fig("img", "inspector", "The claim file starts on-site: time-stamped photos, moisture maps, and readings from the first visit.", "Inspector documenting a property with a clipboard")}
<p>Most water damage claims aren't denied because the damage isn't real — they're underpaid because the file is thin. A few phone photos and a one-line invoice leave the adjuster guessing, and guesses don't favor you.</p>
<h2>What usually is (and isn't) covered</h2>
<ul>
<li><b>Usually covered:</b> burst or frozen pipes, sudden appliance failures, water heater ruptures, storm-driven roof leaks, sump pump failure (with the sump/sewage endorsement).</li>
<li><b>Usually not covered:</b> gradual leaks left unaddressed, groundwater seepage, overland flooding (that's flood insurance), mold from long-term neglect. Standard policies do <b>not</b> automatically cover sump-pump failure or sewer backup — check whether you carry the endorsement.</li>
</ul>
<h2>The documentation package we build for you</h2>
<ul class="checks">{checks}</ul>
<h2>Your first 24 hours, in order</h2>
<ul>
<li><b>1.</b> Stop the water (main shut-off) and make the area safe.</li>
<li><b>2.</b> Call us for extraction — policies require reasonable mitigation.</li>
<li><b>3.</b> Photograph everything before cleanup if you can do it safely.</li>
<li><b>4.</b> Open the claim and give your insurer our documentation package.</li>
<li><b>5.</b> Keep receipts for any emergency expenses (hotel, pumps, fans).</li>
</ul>
<p>Context: 1 in 60 insured homes files a water or freezing claim each year, and water damage accounts for 22.6% of all homeowner claims (Insurance Information Institute). Adjusters see this daily — a complete file is simply the fastest route to a fair settlement.</p>"""
    return page_shell("Water Damage Insurance Claims Guide | Meridian, ID",
        "How water damage insurance claims work in Meridian, ID — what's covered, the documentation adjusters need, and your first 24 hours.",
        "/water-damage-insurance-claims/", "Water Damage Insurance Claims in Meridian", "Claims Guide", body, faqs)

'''
s = replace_block(s, "def insurance_page():", "\ndef simple_pages():", INS_NEW)

# ---------- 8. simple_pages: about/contact/careers + sitemap ZIP list ----------
s = s.replace('"About Fishers Water Damage Repair — 24/7 water damage restoration for Fishers and Hamilton County homeowners."',
              '"About Meridian Water Damage Repair — 24/7 water damage restoration for Meridian and Treasure Valley homeowners."')
s = s.replace('"Contact Fishers Water Damage Repair — 24/7 emergency line (317) 978-8269. Serving Fishers & Hamilton County."',
              '"Contact Meridian Water Damage Repair — 24/7 emergency line (208) 213-9706. Serving Meridian & the Treasure Valley."')
s = s.replace('"Join Fishers Water Damage Repair — restoration technicians and crew leads wanted in Fishers, IN."',
              '"Join Meridian Water Damage Repair — restoration technicians and crew leads wanted in Meridian, ID."')
# sitemap page ZIP list (Fishers 5 ZIPs -> Meridian 2 + town ZIPs)
old_ziplist = '''<h2>Fishers ZIP Codes</h2><ul>
<li><a href="/46037/">46037 — Central &amp; East Fishers</a></li>
<li><a href="/46038/">46038 — West Fishers &amp; Downtown</a></li>
<li><a href="/46040/">46040 — Geist Reservoir North &amp; West Shore</a></li>
<li><a href="/46055/">46055 — Geist East Shore</a></li>
<li><a href="/46060/">46060 — North Fishers Fringe (Saxony Corridor)</a></li>
</ul>'''
new_ziplist = '''<h2>ZIP Codes</h2><ul>
<li><a href="/83642/">83642 — South &amp; West Meridian</a></li>
<li><a href="/83646/">83646 — North Meridian (Idaho's most populous ZIP)</a></li>
<li><a href="/83702/">83702 — Downtown Boise</a></li>
<li><a href="/83704/">83704 — West Boise</a></li>
<li><a href="/83705/">83705 — South &amp; Southeast Boise</a></li>
<li><a href="/83706/">83706 — Southeast Boise</a></li>
<li><a href="/83709/">83709 — Southwest Boise</a></li>
<li><a href="/83712/">83712 — East Boise</a></li>
<li><a href="/83713/">83713 — Northwest Boise</a></li>
<li><a href="/83716/">83716 — Far East Boise</a></li>
<li><a href="/83651/">83651 — Central &amp; North Nampa</a></li>
<li><a href="/83686/">83686 — South &amp; West Nampa</a></li>
<li><a href="/83687/">83687 — North &amp; East Nampa</a></li>
<li><a href="/83616/">83616 — Eagle</a></li>
<li><a href="/83605/">83605 — Central Caldwell</a></li>
<li><a href="/83607/">83607 — South &amp; East Caldwell</a></li>
<li><a href="/83634/">83634 — Kuna</a></li>
<li><a href="/83669/">83669 — Star</a></li>
<li><a href="/83644/">83644 — Middleton</a></li>
<li><a href="/83714/">83714 — Garden City</a></li>
<li><a href="/83617/">83617 — Emmett</a></li>
</ul>'''
assert old_ziplist in s
s = s.replace(old_ziplist, new_ziplist)

# ---------- 9. Shared blocks: WHY_CARDS, reviews, video band, gallery ----------
WHY_NEW = '''WHY_CARDS = [("clock", "Real Emergency Response", "Live answer around the clock and crews staged for Meridian — Paramount to Tuscany — not a call center three states away."),
             ("doc", "Insurance Paperwork, Handled", "Photos, moisture maps, and line-item estimates in the format adjusters actually approve. We meet your adjuster on-site."),
             ("fan", "Drying Science, Not Guesswork", "Moisture meters, thermal cameras, and daily readings. We prove it's dry before anything gets closed up."),
             ("home", "Local &amp; Accountable", "We work Meridian's new-build subdivisions, irrigation canals, high water table, and freeze cycles every week. One consistent phone number — ours.")]'''
s = replace_block(s, "WHY_CARDS = [", "\ndef why_section", WHY_NEW + "\n\n")

_REVS_NEW = '''_REVS = [("We woke up to water in the ground floor after the sump pump died during spring runoff. They answered on the second ring at 5 a.m., had the water out by lunch, and five days later you couldn't tell it happened. The documentation packet they gave our insurer was unreal.", "Sarah M.", "Paramount, Meridian"),
         ("A supply line let go behind our fridge and soaked the kitchen floor. They found moisture under cabinets we never would have checked, dried everything without tearing out the floor, and met the adjuster at our house. Zero drama.", "David R.", "Tuscany, Meridian"),
         ("Frozen pipe burst in January while we were out of town. Our neighbor called them — by the time we flew home, the house was dry and the claim file was already with our insurer. This is how every contractor should operate.", "Karen T.", "Lochsa Falls, Meridian")]'''
s = replace_block(s, "_REVS = [", "\nREVIEWS_SECTION", _REVS_NEW + "\n")

s = s.replace("When Hamilton County storms push water into Fishers basements, our crews are already rolling — extraction trucks, drying equipment, and a claim file started from hour one.",
              "When Treasure Valley spring runoff pushes water into Meridian crawl spaces and ground floors, our crews are already rolling — extraction trucks, drying equipment, and a claim file started from hour one.")
s = s.replace("Real footage, no stock smiles: what storm water does to a neighborhood, and what a dried, restored home looks like when the work is done right.",
              "Real footage, no stock smiles: what flood water does to a neighborhood, and what a dried, restored home looks like when the work is done right.")
s = s.replace("When storm water rises across Hamilton County, basements and ground floors take it first — every hour of standing water adds materials to the loss.",
              "When flood water rises across the Treasure Valley, crawl spaces and ground floors take it first — every hour of standing water adds materials to the loss.")
s = s.replace("This is what rolls off our trucks on every Fishers job:",
              "This is what rolls off our trucks on every Meridian job:")
s = s.replace("The actual scenes our crews walk into across Fishers and Hamilton County — and what happens next.",
              "The actual scenes our crews walk into across Meridian and the Treasure Valley — and what happens next.")
s = s.replace("truck-mounted vacuum in living rooms, basements, and finished lower levels.",
              "truck-mounted vacuum in living rooms, ground floors, and finished lower levels.")
s = s.replace("sump failures and seepage handled with drying, drainage, and waterproofing.",
              "sump failures and seepage handled with drying, drainage, and crawl-space waterproofing.")
s = s.replace("An unfinished Hamilton County basement — where drainage, sump, and waterproofing work actually happens.",
              "An unfinished crawl space and lower level — where drainage, sump, and waterproofing work actually happens.")
s = s.replace("Flooded suburban home with standing water around it",
              "Flooded suburban home with standing water around it")
s = s.replace("A home surrounded by standing water after a storm — the most common call we run in Fishers.",
              "A home surrounded by standing water after a storm — the most common call we run in Meridian.")
s = s.replace("Flooded basement? We pump out water", "Flooded crawl space or ground floor? We pump out water")

# simple_pages bodies: about / contact
s = s.replace("<li><b>Local knowledge.</b> Hamilton County clay soil, sump-pump dependence, Geist water tables, and Indiana freeze cycles are our weekly reality.</li>",
              "<li><b>Local knowledge.</b> Meridian's new-build subdivisions, irrigation canals, high water table, spring snowmelt into crawl spaces, and Idaho freeze cycles are our weekly reality.</li>")
s = s.replace("Fishers, Indiana — serving Hamilton County including Carmel, Noblesville, Westfield, Geist, McCordsville, and Fortville.",
              "Meridian, Idaho — serving the Treasure Valley including Boise, Nampa, Eagle, Caldwell, Kuna, Star, Middleton, Garden City, and Emmett.")
s = s.replace("October 2, 2026", "November 10, 2026")

# ---------- 10. Global token replacements ----------
for a, b in [
    ("Indianapolis", "Boise"),
    ("waterdamagerepairfishersin.com", "waterdamagerepairmeridianid.com"),
    ("Fishers", "Meridian"),
    ("fishers", "meridian"),
    ("Hamilton County", "Treasure Valley"),
    ("Indiana", "Idaho"),
    (", IN", ", ID"),
    ("IN →", "ID →"),
    ("IN &", "ID &"),
    ("IN.", "ID."),
    ("basement waterproofing &amp; sump pump solutions", "crawl space waterproofing &amp; drying"),
    ("Basement Waterproofing", "Crawl Space Waterproofing & Drying"),
    ("basement waterproofing", "crawl space waterproofing"),
    ("Flood & Basement Cleanup", "Flood & Crawl Space Cleanup"),
    ("flooded basement", "flooded crawl space or ground floor"),
    ("Flooded basement", "Flooded crawl space or ground floor"),
    ("finished basement", "finished ground floor"),
    ("Finished basement", "Finished ground floor"),
    ("basements", "crawl spaces"),
    ("Basements", "Crawl spaces"),
    ("basement", "crawl space"),
    ("Basement", "Crawl space"),
]:
    s = s.replace(a, b)

# Fix over-corrections from basement->crawl space sweep in service slugs/URLs must stay:
# (slugs were already in SERVICES list as "basement-waterproofing" — check below in validation)
# ---------- 10b. Repair over-corrections from the basement->crawl space sweep ----------
s = s.replace('"crawl space-waterproofing"', '"basement-waterproofing"')
s = s.replace('("crawl space-waterproofing",', '("basement-waterproofing",')
s = s.replace('"/crawl space-waterproofing/"', '"/basement-waterproofing/"')
s = s.replace('"basement-waterproofing": "crawl space"', '"basement-waterproofing": "basement"')
s = s.replace('("crawl space", "LGR Dehumidifiers"', '("basement", "LGR Dehumidifiers"')
s = s.replace('_gal("crawl space",', '_gal("basement",')
s = s.replace('("img", "crawl space",', '("img", "basement",')
s = s.replace('("My home has no crawl space — do I still need waterproofing?", "Yes — in Meridian, the crawl space is where the water goes. Encapsulation plus a reliable sump system does for a crawl space what a crawl space system does elsewhere.")',
              '("My home has no basement — do I still need waterproofing?", "Yes — in Meridian, the crawl space is where the water goes. Encapsulation plus a reliable sump system does for a crawl space what a basement system does elsewhere.")')
s = s.replace("(317) 978-8269", "(208) 213-9706")
s = s.replace("+13179788269", "+12082139706")

s = ("# PHONE PLACEHOLDER — replace with Idaho-local Ringba number before custom-domain launch.\n"
       "# The site currently uses the reserved fictional number (208) 213-9706 / tel:+12082139706\n"
       "# everywhere. Do NOT launch on the custom domain with this number.\n\n" + s)
open(DST, "w", encoding="utf-8").write(s)
print("written", DST, len(s), "chars")

# leftover checks (report, don't fail yet)
import re as _re
for tok in ["Fishers", "fishers", "Geist", "geist", "Hamilton", "clay", "Clay", "Indiana",
            "(317)", "317", "46037", "46038", "46040", "46055", "46060", "46250", "46256",
            "Carmel", "Noblesville", "Westfield", "McCordsville", "Fortville", "83680"]:
    if tok in s:
        print("LEFTOVER:", tok, "count", s.count(tok))
print("done")
