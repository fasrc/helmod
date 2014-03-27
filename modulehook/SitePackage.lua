require("strict")
local hook   = require("Hook")

-- By using the hook.register function, this function "load_hook" is called
-- ever time a module is loaded with the file name and the module name.


local function sh_quote(text)
   return "'" .. string.gsub(text, "'", "'\\''") .. "'"
end

function load_hook(t)
   -- the arg t is a table:
   --     t.modFullName:  the module full name: (i.e: gcc/4.7.2)
   --     t.fn:           The file name: (i.e /apps/modulefiles/Core/gcc/4.7.2.lua)

   -- Your site can use this any way that suits.  Here are some possibilities:
   --  a) Write this information into a file in your users directory (say ~/.lmod.d/.save).
   --     Then once a month collect this data.
   --  b) have this function call syslogd to register that this module was loaded by this
   --     user
   --  c) Write the same information directly to some database.

   -- This is the directory in which this script resides, and it pulls the rest 
   -- of the required scripts and config from this same directory.  (It would 
   -- be better to compute this, but my lua skills are lacking.)
   local dirname = os.getenv("LMOD_PACKAGE_PATH")

   local username = os.getenv("USER")

   if dirname ~= '' and username ~= '' and t.modFullName ~= '' then
      -- We don't want failure to log to block jobs or give errors.  Make an 
	  -- effort to log things, but ignore anything that goes wrong.  Also do 
	  -- not wait on the subprocess.
      local sh = ''
      sh = sh .. "setsid"
      sh = sh .. " " .. sh_quote(dirname .. "/modulelogger")
      sh = sh .. " -a load"
      sh = sh .. " -u " .. sh_quote(username)
      sh = sh .. " -f " .. sh_quote(t.fn)
      sh = sh .. " " .. sh_quote(t.modFullName)
      sh = sh .. " >/dev/null 2>/dev/null &"
      os.execute(sh)
   end
end


hook.register("load",load_hook)
