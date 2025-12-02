from fastapi import FastAPI, HTTPException
import subprocess
import re

app = FastAPI()

HELPER = "/usr/local/bin/usbip_helper.sh"
SUDO = ["sudo", HELPER]

# Regex to validate busid (e.g., "1-1", "2-3.4")
BUSID_RE = re.compile(r"^[0-9]+(-[0-9]+(\.[0-9]+)*)$")
USBIP_LIST_RE = re.compile(
    r"- busid (\S+) \(([\da-fA-F]{4}:[\da-fA-F]{4})\)\s+(.+?)\s*:\s*(.+?) \([\da-fA-F]{4}:[\da-fA-F]{4}\)",
    re.MULTILINE
)

def run_helper(args):
    """Run usbip-helper via sudo and return output or raise error."""
    try:
        result = subprocess.run(
            ["sudo", HELPER] + args,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise HTTPException(
            status_code=500,
            detail=e.stderr.strip() or "usbip-helper error"
        )


@app.get("/start")
def start_usbipd():
    return run_helper(["start"])


@app.get("/bind/{busid}")
def bind(busid: str):
    if not BUSID_RE.match(busid):
        raise HTTPException(status_code=400, detail="Invalid BUS ID format")
    return run_helper(["bind", busid])


@app.get("/unbind/{busid}")
def unbind(busid: str):
    if not BUSID_RE.match(busid):
        raise HTTPException(status_code=400, detail="Invalid BUS ID format")
    return run_helper(["unbind", busid])


@app.get("/attach/{host}/{port}")
def attach(host: str, port: int):
    return run_helper(["attach", host, str(port)])


@app.get("/detach/{port}")
def detach(port: int):
    return run_helper(["detach", str(port)])

@app.get("/list")
def list_devices():
    output =  run_helper(["list"])
    devices = []
    for busid, vidpid, vendor, product in USBIP_LIST_RE.findall(output):
        devices.append({
            "busid": busid,
            "vidpid": vidpid,
            "vendor": vendor.strip(),
            "product": product.strip()
        })
    return devices
    