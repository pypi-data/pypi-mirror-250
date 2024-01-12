from os import chmod as _chmod
from os.path import abspath as _abspath


def create_service() -> None:
    _chmod(script := _abspath(__file__)[:-10] + "leads_vec.service.sh", 777)
    with open("/etc/systemd/system/leads_vec.service", "w") as f:
        f.write(f"""
        [Unit]
        Description=LEADS VeC
        
        [Service]
        ExecStart=/bin/bash {script}
        
        [Install]
        WantedBy=graphical-session.target
        """)
