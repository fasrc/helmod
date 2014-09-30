# This sets up the environment for usage of lmod, the user-side of fasrcsw.  It
# also handles the conversion from legacy environment modules to lmod.  Once
# the transition starts, this will replace profile::modules


#--- general capability

class fasrcsw::environment::support_legacy {
  #
  # Add support for using legacy modules.  All of this must be able to co-exist
  # with lmod.  This must NOT set the default environment.
  #

  # This logs all module loads to the database (see checkmodule in hpc/rc
  # for querying stats); requires mysql (port 3306) access to hulsmysql.
  file { '/usr/local/bin/module_db_binary':
    source => 'puppet:///modules/fasrcsw/legacy/module_db_binary',
    owner  => root,
    group  => root,
    mode   => '0755',
    backup => false,
  }
  file { '/usr/local/bin/module_db':
    source  => 'puppet:///modules/fasrcsw/legacy/module_db',
    owner   => root,
    group   => root,
    mode    => '0755',
    backup  => false,
    require => File['/usr/local/bin/module_db_binary'],
  }

  file { '/usr/local/bin/legacy-modules.sh':
    source => 'puppet:///modules/fasrcsw/legacy/modules.sh',
    owner  => root,
    group  => root,
    mode   => '0755',
    backup => false,
  }
  file { '/usr/local/bin/legacy-modules.csh':
    source => 'puppet:///modules/fasrcsw/legacy/modules.csh',
    owner  => root,
    group  => root,
    mode   => '0755',
    backup => false,
  }
}

class fasrcsw::environment::support_lmod {
  #
  # Add support for using lmod modules.  All of this must be able to co-exist
  # with legacy modules.  This must NOT set the default environment.
  #

  ##these packages are now in std_pkgs
  #package { 'lua':
  #  #supposed to be 5.1 or 5.2; getting lua-5.1.4-4.1.el6.x86_64 (as of 2013-11-21)
  #  ensure => 'installed',
  #}
  #package { 'lua-devel':
  #  ensure => 'installed',
  #}
  #package { 'lua-filesystem':
  #  ensure => 'installed',
  #}
  #package { 'lua-posix':
  #  ensure => 'installed',
  #}

  file { '/usr/share/zsh/site-functions/_ml':
    source => 'puppet:///modules/fasrcsw/_ml',
    owner  => root,
    group  => root,
  }
  file { '/usr/share/zsh/site-functions/_module':
    source => 'puppet:///modules/fasrcsw/_module',
    owner  => root,
    group  => root,
  }

  file { '/usr/local/bin/lmod.sh':
    source => 'puppet:///modules/fasrcsw/profile',
    owner  => root,
    group  => root,
    mode   => '0755',
    backup => false,
  }
  file { '/usr/local/bin/lmod.csh':
    source => 'puppet:///modules/fasrcsw/cshrc',
    owner  => root,
    group  => root,
    mode   => '0755',
    backup => false,
  }

  #these are just for the opt-in phase
  file { '/usr/local/bin/new-modules.sh':
    source => 'puppet:///modules/fasrcsw/new-modules.sh',
    owner  => root,
    group  => root,
    mode   => '0755',
    backup => false,
  }
  file { '/usr/local/bin/new-modules.csh':
    source => 'puppet:///modules/fasrcsw/new-modules.csh',
    owner  => root,
    group  => root,
    mode   => '0755',
    backup => false,
  }
}


#--- setting the default environment

class fasrcsw::environment::purge_old_files {
  file { [
      '/etc/profile.d/fasrcsw.sh',
      '/etc/profile.d/fasrcsw.csh',
      '/etc/profile.d/lmod.sh',
      '/etc/profile.d/lmod.csh',
    ]:
    ensure => 'absent',
    backup => false,
    purge  => true,
    force  => true,
  }
}

class fasrcsw::environment::default_neither {
  include fasrcsw::environment::purge_old_files
  include fasrcsw::environment::support_legacy
  include fasrcsw::environment::support_lmod
}

class fasrcsw::environment::default_legacy {
  include fasrcsw::environment::purge_old_files
  include fasrcsw::environment::support_legacy
  include fasrcsw::environment::support_lmod

  file { '/etc/profile.d/modules.sh':
    ensure  => link,
    target  => '/usr/local/bin/legacy-modules.sh',
    backup  => false,
    force   => true,
    require => [
      File['/usr/local/bin/legacy-modules.sh'],
      File['/etc/profile.d/lmod.sh'],  #(i.e. require absent)
      File['/etc/profile.d/fasrcsw.sh'],  #(i.e. require absent)
    ]
  }
  file { '/etc/profile.d/modules.csh':
    ensure  => link,
    target  => '/usr/local/bin/legacy-modules.csh',
    backup  => false,
    force   => true,
    require => [
      File['/usr/local/bin/legacy-modules.csh'],
      File['/etc/profile.d/lmod.csh'],  #(i.e. require absent)
      File['/etc/profile.d/fasrcsw.csh'],  #(i.e. require absent)
    ]
  }

  file { '/etc/profile.d/module_flavor.sh':
    source  => 'puppet:///modules/fasrcsw/module_flavor_legacy.sh',
    owner   => root,
    group   => root,
    mode    => '0644',
    backup  => false,
    force   => true,
    require => [
      File['/etc/profile.d/modules.sh'],
    ]
  }

  file { '/etc/profile.d/module_flavor.csh':
    source  => 'puppet:///modules/fasrcsw/module_flavor_legacy.csh',
    owner   => root,
    group   => root,
    mode    => '0644',
    backup  => false,
    force   => true,
    require => [
      File['/etc/profile.d/modules.csh'],
    ]
  }
}

class fasrcsw::environment::default_lmod {
  include fasrcsw::environment::purge_old_files
  include fasrcsw::environment::support_legacy
  include fasrcsw::environment::support_lmod

  file { '/etc/profile.d/modules.sh':
    ensure  => link,
    target  => '/usr/local/bin/lmod.sh',
    backup  => false,
    force   => true,
    require => [
      File['/usr/local/bin/lmod.sh'],
      File['/etc/profile.d/lmod.sh'],  #(i.e. require absent)
      File['/etc/profile.d/fasrcsw.sh'],  #(i.e. require absent)
    ]
  }
  file { '/etc/profile.d/modules.csh':
    ensure  => link,
    target  => '/usr/local/bin/lmod.csh',
    backup  => false,
    force   => true,
    require => [
      File['/usr/local/bin/lmod.csh'],
      File['/etc/profile.d/lmod.csh'],  #(i.e. require absent)
      File['/etc/profile.d/fasrcsw.csh'],  #(i.e. require absent)
    ]
  }

  file { '/etc/profile.d/module_flavor.sh':
    source  => 'puppet:///modules/fasrcsw/module_flavor_lmod.sh',
    owner   => root,
    group   => root,
    mode    => '0644',
    backup  => false,
    force   => true,
    require => [
      File['/etc/profile.d/modules.sh'],
    ]
  }

  file { '/etc/profile.d/module_flavor.csh':
    source  => 'puppet:///modules/fasrcsw/module_flavor_lmod.csh',
    owner   => root,
    group   => root,
    mode    => '0644',
    backup  => false,
    force   => true,
    require => [
      File['/etc/profile.d/modules.csh'],
    ]
  }
}
