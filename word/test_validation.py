import unittest
from validation import is_valid_email, clean_and_verify_url

class TestValidation(unittest.TestCase):
    def test_is_valid_email_valid_cases(self):
        """Test valid email addresses."""
        valid_emails = [
            "user@example.com",
            "user.name@sub.domain.co.uk",
            "user+test@company.org",
            "special!#$%&'*+/=?^_`{|}~@domain.com",
            "a@b.co",
            "a" * 64 + "@domain.com",
            "user@" + "a"*63 + "." + "b"*63 + "." + "c"*63 + ".com",
        ]
        for email in valid_emails:
            with self.subTest(email=email):
                self.assertEqual(is_valid_email(email), email)

    def test_is_valid_email_invalid_cases(self):
        """Test invalid email addresses."""
        invalid_emails = [
            "user@.com",
            "user..name@domain.com",  # Consecutive dots
            "user@domain",
            "@domain.com",
            "user@domain.c",
            "user@-domain.com",
            "user@domain..com",
            ".user@domain.com",
            "user.@domain.com",
            "a" * 65 + "@domain.com",  # Local part too long
            "user@" + "a" * 252 + ".com",  # Domain too long
            "a" * 255 + "@domain.com",  # Total length too long
        ]
        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertIsNone(is_valid_email(email))

    def test_is_valid_email_edge_cases(self):
        """Test edge cases for email validation."""
        edge_cases = [
            "",  # Empty string
            None,  # None
            123,  # Non-string
            " " * 100,  # Whitespace
            "üser@exämple.com",  # Unicode (unsupported in current regex)
        ]
        for case in edge_cases:
            with self.subTest(case=case):
                self.assertIsNone(is_valid_email(case))

    def test_clean_and_verify_url_valid_cases(self):
        """Test valid URLs with various components."""
        valid_urls = [
            ("https://www.example.com", "example.com"),
            ("http://sub.domain.co.uk/path?query#fragment", "sub.domain.co.uk/path?query#fragment"),
            ("example.com:8080", "example.com:8080"),
            ("https://192.168.1.1/path", "192.168.1.1/path"),
            ("www.google.com/search?q=test", "google.com/search?q=test"),
            ("localhost", "localhost"),
            ("[2001:db8::1]", "[2001:db8::1]"),
        ]
        for url, expected in valid_urls:
            with self.subTest(url=url):
                self.assertEqual(clean_and_verify_url(url), expected)

    def test_clean_and_verify_url_invalid_cases(self):
        """Test invalid URLs."""
        invalid_urls = [
            "https://.com",
            "http://-domain.com",
            "example..com",
            "256.256.256.256",  # Invalid IP
            "http://",  # No netloc
            "ftp://example.com",  # Unsupported scheme
        ]
        for url in invalid_urls:
            with self.subTest(url=url):
                self.assertIsNone(clean_and_verify_url(url))

    def test_clean_and_verify_url_edge_cases(self):
        """Test edge cases for URL validation."""
        edge_cases = [
            ("", None),  # Empty string
            (None, None),  # None
            (123, None),  # Non-string
            (" " * 100, None),  # Whitespace
            ("example.com///", "example.com"),  # Trailing slashes
            ("example.com:99999", None),  # Invalid port
        ]
        for url, expected in edge_cases:
            with self.subTest(url=url):
                self.assertEqual(clean_and_verify_url(url), expected)

if __name__ == "__main__":
    unittest.main()