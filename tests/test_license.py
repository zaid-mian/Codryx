import unittest
from typing import Any, Dict
from pyguardian.license import license_graph, license_conflicts


def fake_fetch(pkg: str) -> Dict[str, Any]:
    data = {
        "rootpkg": {"info": {"license": "MIT", "requires_dist": ["childpkg (>=1.0)"]}},
        "childpkg": {"info": {"license": "GPL-3.0", "requires_dist": []}},
    }
    return data.get(pkg, {"info": {"license": None, "requires_dist": []}})


class TestLicense(unittest.TestCase):
    def test_conflicts_detection(self):
        declared = {"rootpkg": {"declared": "1.0.0", "latest": "1.2.0", "outdated": "yes"}}
        graph = license_graph(declared, fetcher=fake_fetch)
        conflicts = license_conflicts(graph, ["GPL-3.0"])
        self.assertTrue(any(c[0] == "childpkg" for c in conflicts))


if __name__ == "__main__":
    unittest.main()
