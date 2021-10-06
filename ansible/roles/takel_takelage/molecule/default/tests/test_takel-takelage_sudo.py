import takeltest

testinfra_hosts = takeltest.hosts()


def test_takel_takelage_sudo_passwordless(host, testvars):
    with host.sudo():
        file = host.file('/etc/sudoers')
        sudoline = '%sudo ALL = (ALL) NOPASSWD: ALL'

        assert file.exists
        assert file.is_file
        assert file.user == 'root'
        assert file.group == 'root'
        assert file.mode == 0o440
        assert sudoline in file.content_string
