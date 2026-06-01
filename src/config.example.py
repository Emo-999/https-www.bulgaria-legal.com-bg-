"""Bulgaria Legal — CloudCart redesign configuration (EXAMPLE).
Copy to `config.py` and fill in the CloudCart PAT token (kept out of git).
"""

# CloudCart API
CC_PAT_TOKEN = "cc_pat_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
CC_STORE = "6xm54.cloudcart.net"
CC_GQL_URL = "https://6xm54.cloudcart.net/api/gql"
CC_REST_URL = "https://6xm54.cloudcart.net/api/v2"

# Source site
SRC_URL = "https://www.bulgaria-legal.com"

# Paths
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
