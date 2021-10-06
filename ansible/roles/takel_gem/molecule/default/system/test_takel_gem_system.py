import pytest
import takeltest

testinfra_hosts = takeltest.hosts()


@pytest.fixture(scope='module', name='thor_file')
def put_thor_file(host, moleculebook):
    thor_file_path = '/tmp/thor_file.rb'
    thor_file_content = """\
#!/usr/bin/env ruby
require 'thor'

class MyCLI < Thor
desc 'hello NAME', 'say hello to NAME'
  def hello(name)
    puts "Hello #{name}"
  end
end

MyCLI.start(ARGV)"""

    playbook = moleculebook.get()
    args = dict(content=thor_file_content,
                dest=thor_file_path,
                mode='0755')
    task = dict(action=dict(module='copy',
                            args=args))
    playbook['tasks'].append(task)
    moleculebook.set(playbook)
    moleculebook.run()

    thor_file = host.file(thor_file_path)

    assert thor_file.exists
    assert thor_file.is_file
    assert thor_file.mode == 0o755
    assert thor_file.content_string == thor_file_content


@pytest.fixture(scope='module', name='thor_output')
def get_thor_output(host, thor_file):
    return host.check_output('/tmp/thor_file.rb hello World')


def test_takel_thor_system_available(thor_output):
    assert thor_output == 'Hello World'
