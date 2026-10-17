# Per-video settings: chalkboards, metadata text, background mode per art theme.
CHALK = {
 13: dict(title="How Old Is Oasis Water?", sub="Ages measured from rare atoms in the water",
          rows=[("Siwa's springs", "30,000-50,000 yrs", "estimated age", 'y', "Water feeding the springs"),
                ("Nubian aquifer", "up to 1,000,000 yrs", "krypton-81, 2004", 'c', "In 2004"),
                ("Flow speed", "1-2 m", "per year", 'y', "It moves north")],
          concl=("Ancient rain, still on the move", "meters a year"),
          src="Source: Sturchio et al. (2004) · EGU blog on Siwa (2014)"),
 16: dict(title="A Hole Dug by Wind", sub="The Qattara Depression, northwestern Egypt",
          rows=[("Lowest point", "-133 m", "below sea level", 'c', "Its lowest point"),
                ("Made by", "wind + salt", "deflation", 'y', "Scientists think wind"),
                ("Floor", "salt marshes", "damp ground", 'y', "Its floor")],
          concl=("The wind dug down to the water", "kept damp"),
          src="Source: Wikipedia, Qattara Depression"),
 34: dict(title="The Great Man-Made River", sub="Libya's fossil-water pipeline",
          rows=[("Pipe width", "4 m", "buried concrete", 'y', "four meters wide"),
                ("Network", "~4,000 km", "planned length", 'y', "nearly four thousand"),
                ("Design flow", "~6 million m³", "per day", 'c', "close to six million")],
          concl=("From aquifers barely being refilled", "barely being refilled"),
          src="Source: Canadian Consulting Engineer · Wikipedia"),
 40: dict(title="Rivers Under the Sand", sub="What shuttle radar saw in the eastern Sahara",
          rows=[("Flight", "1981", "Space Shuttle Columbia", 'y', "In November 1981"),
                ("Radar depth", "several m", "in very dry sand", 'y', "see down several meters"),
                ("Buried valleys", "10-15 km", "wide", 'c', "ten to fifteen kilometers")],
          concl=("Radar rivers point to hidden water", "radar rivers"),
          src="Source: AramcoWorld (1983) · USGS"),
}
WHOOSH = []
TITLE = "How Desert Oases Are Really Made"
DESC = ["In the driest deserts on Earth, clear springs and palm groves appear out of the sand. Where does that water come from? Some of it fell as rain in a green Sahara thousands of years ago, and some has been underground for hundreds of thousands of years.",
        "In this video, we follow oasis water from distant mountains into stone aquifers, through artesian pressure, faults, wind-dug depressions and wadis, and look at the date palm, the qanat, the Silk Road, Libya's Great Man-Made River, fog nets and the risks of pumping fossil water."]
CHAPTERS = [(1, "An Ocean of Sand"), (4, "Why Deserts Are Dry"), (6, "Stone Sponges"), (8, "Artesian Pressure"),
            (11, "Fossil Water"), (14, "Carved by Wind"), (17, "Faults as Highways"), (19, "Flash Floods and Wadis"),
            (22, "Seeds and Date Palms"), (26, "The Qanat"), (29, "The Silk Road"), (30, "Sand and Salt"),
            (32, "The Age of the Pump"), (35, "New Water Sources"), (38, "Islands of Evolution"), (44, "Not One Accident")]
SOURCES = ["Sturchio et al. (2004), One million year old groundwater in the Sahara revealed by krypton-81 and chlorine-36, Geophysical Research Letters",
           "McCauley et al. (1982), Subsurface valleys and geoarcheology of the eastern Sahara revealed by shuttle radar, Science",
           "UNESCO World Heritage: Al-Ahsa Oasis; The Persian Qanat",
           "USGS EarthView: Saudi wheat experiment relied on fossil water",
           "Wikipedia: Oasis; Aquifer; Artesian aquifer; Qattara Depression; Siwa Oasis; Great Man-Made River; Fog collection"]
HASHTAGS = "#MiyasLab #Oasis #Desert #Geology #Water"
BG = dict(dunes='dusk', mirage='paper', island='dusk', globe='night', underground='paper', sponge='paper', mountains='dusk',
          layers='paper', artesian='night', siwa='dusk', greensahara='paper', fossilwater='night', wind='dusk', watertable='paper',
          fault='night', coachella='dusk', flashflood='night', gravel='paper', nile='dusk', birds='paper', datepalm='dusk',
          tiers='paper', alahsa='dusk', qanat='paper', tunnel='night', worldmap='paper', silkroad='dusk', barchan='paper',
          salt='night', pump='paper', dryspring='dusk', desal='night', fog='paper', swales='dusk', pools='night', wildlife='dusk',
          subsidence='paper', sharing='night', climate='dusk', summary='paper', ending='dusk')
# Palettes (guideline 3-5): desert sand, oases and history -> desert; underground water, springs, aquifers, fog -> ocean; the Green Sahara -> forest
PAL_DEFAULT = 'desert'
PAL = dict(underground='ocean', sponge='ocean', layers='ocean', artesian='ocean', fossilwater='ocean', watertable='ocean',
           gravel='ocean', tunnel='ocean', subsidence='ocean', pools='ocean', fog='ocean', greensahara='forest',
           )

HOOK = dict(until=300, maxu=5.5)   # guideline 20-2 (2026-10-17 remake): denser first 5 minutes; minimum on-screen time 3.5 s (minu) applied by build3
