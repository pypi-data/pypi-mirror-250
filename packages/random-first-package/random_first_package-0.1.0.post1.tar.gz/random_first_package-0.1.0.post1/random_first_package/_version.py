import os
import logging
import re

BASE_VERSION = "0.1.0"

def get_version():

    version_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'VERSION')
    logging.info(f"Reading version from: {version_file}")

    try:
        with open(version_file) as f:
            version_str = f.read().strip()
            logging.info(f"Version string: {version_str}")

            # Regular expression to parse the version components
            version_pattern = r'(\d+\.\d+\.\d+)(?:\.(dev|alpha|beta|rc)\d+)?\+g([0-9a-f]+)\.d\d+'
            match = re.match(version_pattern, version_str)

            if match:
                _, dev_status, git_hash = match.groups()
                post_version = '0' if dev_status is None else '1'
                # Construct PEP 440 compliant version (post-release format)
                pep440_version = f"{BASE_VERSION}.post{post_version}"
                return pep440_version
            
            raise ValueError(f"Invalid version string: {version_str}")
            
    except FileNotFoundError:
        logging.error(f"Could not find {version_file}")
        return "not_found_version"
