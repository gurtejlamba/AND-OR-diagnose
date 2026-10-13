"""
Device-specific AND-OR problem trees.

Structure
---------
OR  node  → try alternatives; AO* picks the cheapest sub-tree.
AND node  → ALL children must be done (sequential diagnostic steps).
LEAF node → a concrete repair action with a known cost and time.
"""

from .and_or_graph import Node, NodeType

# ──────────────────────────────────────────────────────────────────────
# Problem 1 : Laptop Won't Start
# ──────────────────────────────────────────────────────────────────────

def build_laptop_wont_start() -> Node:
    root = Node(
        "Laptop Won't Start", NodeType.OR, h_cost=50,
        description="Laptop does not power on or fails to boot to OS",
    )

    # ── software issue (cheapest, try first) ──
    software = Node("Software Issue", NodeType.OR, h_cost=5,
                    description="OS or bootloader corruption")
    software.add_child(Node("Boot in Safe Mode", NodeType.LEAF, cost=0, fix_time=10,
        description="Press F8 / Shift at startup; diagnose drivers"))
    software.add_child(Node("Run Startup Repair", NodeType.LEAF, cost=0, fix_time=30,
        description="Use Windows Recovery / macOS Disk Utility to repair boot"))
    # AND: a reinstall wipes the disk, so the backup has to happen too
    reinstall = Node("Clean OS Reinstall", NodeType.AND, h_cost=0,
                     description="Back up, then reinstall — both steps required")
    reinstall.add_child(Node("Back Up Your Files", NodeType.LEAF, cost=0, fix_time=30,
        description="Boot from USB or remove the drive; copy personal files off"))
    reinstall.add_child(Node("Reinstall OS", NodeType.LEAF, cost=0, fix_time=90,
        description="Clean OS install from recovery media"))
    software.add_child(reinstall)

    # ── power issue ──
    power = Node("Power Issue", NodeType.OR, h_cost=20,
                 description="Charger, battery, or power rail problem")
    power.add_child(Node("Static Discharge Reset", NodeType.LEAF, cost=0, fix_time=3,
        description="Hold power 30 s with battery and charger removed"))
    power.add_child(Node("Test / Replace Charger", NodeType.LEAF, cost=15, fix_time=5,
        description="Try a known-good charger; replace if faulty"))
    power.add_child(Node("Replace Battery", NodeType.LEAF, cost=50, fix_time=30,
        description="Install new OEM or compatible battery"))

    # ── display issue ──
    display = Node("Display Issue", NodeType.OR, h_cost=30,
                   description="Laptop powers on but screen stays blank")
    display.add_child(Node("Test External Monitor", NodeType.LEAF, cost=0, fix_time=5,
        description="Plug in HDMI / VGA monitor to isolate display vs. GPU"))
    display.add_child(Node("Reseat Display Cable", NodeType.LEAF, cost=0, fix_time=20,
        description="Open lid bezel; unplug and re-plug internal LVDS/eDP cable"))
    display.add_child(Node("Replace Screen", NodeType.LEAF, cost=120, fix_time=60,
        description="Swap LCD/LED panel with matching model"))

    # ── hardware issue ──
    hardware = Node("Hardware Issue", NodeType.OR, h_cost=80,
                    description="Physical component failure on mainboard or storage")
    hardware.add_child(Node("Reseat RAM", NodeType.LEAF, cost=0, fix_time=15,
        description="Remove and firmly reinsert all RAM sticks"))
    # AND: a new drive is blank until the OS is put back on it
    drive = Node("Drive Replacement", NodeType.AND, h_cost=70,
                 description="Swap the drive, then restore the system — both steps required")
    drive.add_child(Node("Install New SSD / HDD", NodeType.LEAF, cost=70, fix_time=45,
        description="Fit a compatible SSD in the drive bay"))
    drive.add_child(Node("Restore OS & Files", NodeType.LEAF, cost=0, fix_time=60,
        description="Install the OS on the new drive and copy files back"))
    hardware.add_child(drive)
    hardware.add_child(Node("Replace Motherboard", NodeType.LEAF, cost=280, fix_time=120,
        description="Full board swap — last resort"))

    root.add_child(software)
    root.add_child(power)
    root.add_child(display)
    root.add_child(hardware)
    return root


# ──────────────────────────────────────────────────────────────────────
# Problem 2 : WiFi Not Working
# ──────────────────────────────────────────────────────────────────────

def build_wifi_not_working() -> Node:
    root = Node(
        "WiFi Not Working", NodeType.OR, h_cost=10,
        description="Device cannot detect or connect to any WiFi network",
    )

    # software fixes
    soft = Node("Software Fix", NodeType.OR, h_cost=0,
                description="Driver or OS-level WiFi stack issues")
    soft.add_child(Node("Toggle WiFi Off / On", NodeType.LEAF, cost=0, fix_time=1,
        description="Disable then re-enable the WiFi adapter"))
    soft.add_child(Node("Restart Device", NodeType.LEAF, cost=0, fix_time=3,
        description="Full reboot clears driver state"))
    soft.add_child(Node("Update / Reinstall Driver", NodeType.LEAF, cost=0, fix_time=15,
        description="Download latest WiFi driver from manufacturer site"))
    # AND: resetting the stack also drops saved networks, so you must rejoin
    net_reset = Node("Full Network Reset", NodeType.AND, h_cost=0,
                     description="Forget, reset and rejoin — all steps required")
    net_reset.add_child(Node("Forget the Network", NodeType.LEAF, cost=0, fix_time=1,
        description="Remove the saved WiFi network from the device"))
    net_reset.add_child(Node("Reset Network Stack", NodeType.LEAF, cost=0, fix_time=10,
        description="Run: netsh winsock reset  (Win) / renew DHCP lease (macOS/Linux)"))
    net_reset.add_child(Node("Rejoin with Password", NodeType.LEAF, cost=0, fix_time=2,
        description="Select the network again and enter the WiFi password"))
    soft.add_child(net_reset)

    # router / ISP fixes
    router = Node("Router / ISP Fix", NodeType.OR, h_cost=0,
                  description="Problem is on the router or ISP side")
    router.add_child(Node("Restart Router & Modem", NodeType.LEAF, cost=0, fix_time=2,
        description="Power-cycle both devices for 30 s"))
    router.add_child(Node("Check ISP Outage", NodeType.LEAF, cost=0, fix_time=10,
        description="Visit ISP status page or call support"))
    # AND: a factory reset erases the router's settings, so they must be re-entered
    router_reset = Node("Router Factory Reset", NodeType.AND, h_cost=0,
                        description="Reset the router, then set it up again — both steps required")
    router_reset.add_child(Node("Reset Router to Factory Settings", NodeType.LEAF, cost=0, fix_time=5,
        description="Hold the reset pin for 10 s until the lights blink"))
    router_reset.add_child(Node("Set Up Network Name & Password", NodeType.LEAF, cost=0, fix_time=15,
        description="Log in to the router admin page and recreate the WiFi network"))
    router.add_child(router_reset)

    # hardware fixes
    hw = Node("Hardware Fix", NodeType.OR, h_cost=30,
              description="Internal WiFi card fault")
    hw.add_child(Node("Reseat WiFi Card", NodeType.LEAF, cost=0, fix_time=20,
        description="Open laptop; reseat M.2 / mini-PCIe WiFi card"))
    hw.add_child(Node("Use USB WiFi Adapter", NodeType.LEAF, cost=15, fix_time=5,
        description="Plug in an external USB dongle as a workaround"))
    # AND: a new card gets no signal until the antennas are reconnected
    card = Node("WiFi Card Replacement", NodeType.AND, h_cost=25,
                description="Fit the card and reconnect its antennas — both steps required")
    card.add_child(Node("Install New WiFi Card", NodeType.LEAF, cost=25, fix_time=30,
        description="Swap the M.2 / mini-PCIe card with a compatible model"))
    card.add_child(Node("Reconnect Antenna Cables", NodeType.LEAF, cost=0, fix_time=10,
        description="Clip both antenna leads onto the new card"))
    hw.add_child(card)

    root.add_child(soft)
    root.add_child(router)
    root.add_child(hw)
    return root


# ──────────────────────────────────────────────────────────────────────
# Problem 3 : Phone Overheating
# ──────────────────────────────────────────────────────────────────────

def build_phone_overheating() -> Node:
    root = Node(
        "Phone Overheating", NodeType.OR, h_cost=10,
        description="Smartphone body becomes dangerously hot during use or charging",
    )

    # app / software
    app = Node("App / Software Issue", NodeType.OR, h_cost=0,
               description="Runaway background process consuming CPU/GPU")
    app.add_child(Node("Force-Close Background Apps", NodeType.LEAF, cost=0, fix_time=2,
        description="Open task manager; kill all background processes"))
    app.add_child(Node("Identify & Remove Drain App", NodeType.LEAF, cost=0, fix_time=10,
        description="Check battery usage stats; uninstall culprit app"))
    # AND: a reset wipes the phone, so back up first and reinstall after
    wipe = Node("Clean Factory Reset", NodeType.AND, h_cost=0,
                description="Back up, wipe, reinstall — all steps required")
    wipe.add_child(Node("Back Up Phone", NodeType.LEAF, cost=0, fix_time=20,
        description="Back up photos, contacts and app data to the cloud or a computer"))
    wipe.add_child(Node("Factory Reset", NodeType.LEAF, cost=0, fix_time=30,
        description="Full wipe — eliminates all software causes"))
    wipe.add_child(Node("Reinstall Apps One by One", NodeType.LEAF, cost=0, fix_time=40,
        description="Add apps back gradually and watch the temperature"))
    app.add_child(wipe)

    # charging-related
    charge = Node("Charging Related", NodeType.OR, h_cost=5,
                  description="Heat generated specifically while charging")
    charge.add_child(Node("Remove Case While Charging", NodeType.LEAF, cost=0, fix_time=1,
        description="Phone case traps heat — charge without it"))
    charge.add_child(Node("Replace Charger / Cable", NodeType.LEAF, cost=20, fix_time=5,
        description="Faulty charger can push wrong voltage; swap for OEM"))

    # hardware
    hw = Node("Hardware Issue", NodeType.OR, h_cost=80,
              description="Physical component failure causing excess heat")
    # AND: confirm the battery is the culprit before paying to replace it
    battery = Node("Battery Replacement", NodeType.AND, h_cost=40,
                   description="Check the battery, then replace it — both steps required")
    battery.add_child(Node("Check Battery Health", NodeType.LEAF, cost=0, fix_time=5,
        description="Settings → Battery → Health; look for swelling or low capacity"))
    battery.add_child(Node("Replace Battery", NodeType.LEAF, cost=40, fix_time=30,
        description="Swollen or degraded cell generates excessive heat"))
    hw.add_child(battery)
    hw.add_child(Node("Professional Repair", NodeType.LEAF, cost=100, fix_time=120,
        description="Thermal paste reapplication or IC-level board repair"))

    root.add_child(app)
    root.add_child(charge)
    root.add_child(hw)
    return root


# ──────────────────────────────────────────────────────────────────────
# Problem 4 : Printer Not Printing
# ──────────────────────────────────────────────────────────────────────

def build_printer_not_printing() -> Node:
    root = Node(
        "Printer Not Printing", NodeType.OR, h_cost=15,
        description="Printer is powered but produces no output",
    )

    # connection check (AND: must verify both cable AND driver)
    connection = Node("Connection Diagnosis", NodeType.AND, h_cost=0,
                      description="Verify physical and logical connection — all steps required")
    connection.add_child(Node("Check & Reseat USB / Network Cable", NodeType.LEAF, cost=0, fix_time=3,
        description="Ensure cable is firmly seated at both ends"))
    connection.add_child(Node("Reinstall Printer Driver", NodeType.LEAF, cost=0, fix_time=15,
        description="Remove old driver; install latest from manufacturer"))

    # consumables
    consumables = Node("Consumables Issue", NodeType.OR, h_cost=20,
                       description="Paper or ink/toner problem")
    consumables.add_child(Node("Clear Paper Jam", NodeType.LEAF, cost=0, fix_time=5,
        description="Open all covers; remove jammed paper carefully"))
    # AND: a new cartridge prints badly until the heads are aligned to it
    cartridge = Node("New Cartridge", NodeType.AND, h_cost=30,
                     description="Fit the cartridge, then align it — both steps required")
    cartridge.add_child(Node("Replace Ink / Toner Cartridge", NodeType.LEAF, cost=30, fix_time=10,
        description="Install fresh cartridge matching printer model"))
    cartridge.add_child(Node("Run Print Head Alignment", NodeType.LEAF, cost=0, fix_time=5,
        description="Run the alignment utility from the printer menu"))
    consumables.add_child(cartridge)

    # hardware
    hw = Node("Hardware Fault", NodeType.OR, h_cost=60,
              description="Internal print mechanism or board failure")
    hw.add_child(Node("Clean Print Heads", NodeType.LEAF, cost=0, fix_time=20,
        description="Run built-in head-cleaning utility 2-3 times"))
    hw.add_child(Node("Replace Print Head Assembly", NodeType.LEAF, cost=55, fix_time=45,
        description="Swap the removable print head module"))
    hw.add_child(Node("Replace Printer", NodeType.LEAF, cost=120, fix_time=30,
        description="Board failure — replacement is cheaper than board repair"))

    root.add_child(connection)
    root.add_child(consumables)
    root.add_child(hw)
    return root


# ──────────────────────────────────────────────────────────────────────
# Registry
# ──────────────────────────────────────────────────────────────────────

DEVICE_PROBLEMS = {
    "1": ("Laptop Won't Start",    build_laptop_wont_start),
    "2": ("WiFi Not Working",      build_wifi_not_working),
    "3": ("Phone Overheating",     build_phone_overheating),
    "4": ("Printer Not Printing",  build_printer_not_printing),
}
