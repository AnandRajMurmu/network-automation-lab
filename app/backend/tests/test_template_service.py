import unittest

from jinja2.exceptions import TemplateNotFound, UndefinedError
from services.template_service import render_template


class TestTemplateService(unittest.TestCase):
    def setUp(self):
        self.variables = {
            "hostname": "DIST-SW1",
            "domain_name": "lab.local",
            "management_vlan": 30,
            "management_ip": "192.168.30.11",
            "subnet_mask": "255.255.255.0",
            "default_gateway": "192.168.30.254",
        }

    def test_render_base_switch_configuration(self):
        configuration = render_template(
            "cisco/base_switch.j2",
            self.variables,
        )

        self.assertIn("hostname DIST-SW1", configuration)
        self.assertIn("ip domain-name lab.local", configuration)
        self.assertIn("interface Vlan30", configuration)
        self.assertIn(
            "ip address 192.168.30.11 255.255.255.0",
            configuration,
        )
        self.assertIn("ip default-gateway 192.168.30.254", configuration)

    def test_missing_variable_raises_error(self):
        variables = self.variables.copy()
        del variables["hostname"]

        with self.assertRaises(UndefinedError):
            render_template("cisco/base_switch.j2", variables)

    def test_nonexistent_template_raises_error(self):
        with self.assertRaises(TemplateNotFound):
            render_template(
                "cisco/nonexistent.j2",
                self.variables,
            )

    def test_invalid_template_paths_are_rejected(self):
        invalid_paths = [
            "../outside.j2",
            "/etc/passwd.j2",
            "cisco/base_switch.txt",
        ]

        for template_name in invalid_paths:
            with (
                self.subTest(template_name=template_name),
                self.assertRaises(ValueError),
            ):
                render_template(template_name, self.variables)


if __name__ == "__main__":
    unittest.main()
