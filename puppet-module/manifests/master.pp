# Some basic things for fasrcsw.  Only one host should get this.  The
# filesystem on which $FASRCSW_PROD lives must also be un-root-squashed to any
# host that gets this.

class fasrcsw::master {
  #--- logging hook

  file { '/n/sw/fasrcsw/modulehook/.my.cnf.modulelogger':
    # This is the world-usable account for inserts, therefore the creds are
    # world-readable.
    source => 'puppet:///modules/fasrcsw/.my.cnf.modulelogger',
    owner  => root,
    group  => root,
  }

  file { '/n/sw/fasrcsw/modulehook/.my.cnf.modulestats':
    # This is the admin-usable account for reporting, therefore the creds
    # are not world-readable.  However, its only power is to select module
    # usage statistics, so it's not a big deal if this were to be
    # compromised.
    source => 'puppet:///modules/fasrcsw/.my.cnf.modulestats',
    owner  => root,
    group  => rc_admin,
    mode   => '0640',
  }
}
