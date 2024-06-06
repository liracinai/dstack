import subprocess
import unittest
from unittest.mock import MagicMock, patch

from dstack._internal.utils.ssh import check_required_ssh_version


class TestCheckRequiredSSHVersion(unittest.TestCase):
    @patch("subprocess.run")
    def test_ssh_version_above_8_4(self, mock_run):
        # Mock subprocess.run to return a version above 8.4
        mock_run.return_value = MagicMock(returncode=0, stderr="OpenSSH_8.6p1, LibreSSL 3.3.6")

        self.assertTrue(check_required_ssh_version())

    @patch("subprocess.run")
    def test_ssh_version_exactly_8_4(self, mock_run):
        # Mock subprocess.run to return version 8.4
        mock_run.return_value = MagicMock(returncode=0, stderr="OpenSSH_8.4p1, LibreSSL 3.2.3")

        self.assertTrue(check_required_ssh_version())

    @patch("subprocess.run")
    def test_subprocess_error(self, mock_run):
        # Mock subprocess.run to raise a CalledProcessError
        mock_run.side_effect = subprocess.CalledProcessError(returncode=1, cmd="ssh -V")

        self.assertTrue(check_required_ssh_version())

    @patch("subprocess.run")
    def test_ssh_version_on_windows(self, mock_run):
        # Mock subprocess.run to return version 8.4
        mock_run.return_value = MagicMock(
            returncode=0, stdout="OpenSSH_for_Windows_8.1p1, LibreSSL 3.2.3", stderr=""
        )
        # Should ignore windows check

        self.assertTrue(check_required_ssh_version())


if __name__ == "__main__":
    unittest.main()
