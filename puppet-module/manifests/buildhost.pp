# The host(s) where app building takes place.  The filesystem on which
# $FASRCSW_PROD lives must also be un-root-squashed to any host that gets this.

class fasrcsw::buildhost {
  package { [
      'rpm-build',
      'redhat-rpm-config',
      'make',
      'gcc',
    ]:
    ensure => 'installed',
  }
}
