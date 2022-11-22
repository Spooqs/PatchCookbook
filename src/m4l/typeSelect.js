autowatch = 1
inlets = 1
outlets = 2

var target_device_name = null;
var dictionary_name = null;

function targetdevice(name) {
	target_device_name = name;
	bang();
}

function dictionary(name) {
	
	post("dictionary seen on inlet " + inlet + "\n")
	dictionary_name = name;
	bang();
}

function bang() {
	
	if (target_device_name && dictionary_name) {
		post("TYPESELECT \n");
		post("running with dict = `" + dictionary_name + "`\n");
		post("running with target = `" + target_device_name + "`\n");
	
		var fullDict = new Dict(dictionary_name);
	
	
		var devDict = fullDict.get(target_device_name);
		
		if (! devDict) {
			post(target_device_name + " not found in patches file\n");
			return null;
		}
			
	
		keys = devDict.getkeys()
		
		if ( keys === null || keys.length == 0) {
			post("No categories found for " + target_device_name + "\n");
			return null;
		}
		

		// We are going to send all the keys items again.
		// So force the umenu to clear. This probably ought
		// to go out a separate port, but I don know how to handle timing
		// This is will do for now.
	
		outlet(0, "clear")
		
		// If there is only on category, then m4l returns a string
		// rather than an Array with one object. So, we need to check
		// what we have to be able to handle it. Silly.
	
		if ( keys instanceof Array) {
			// Run through the array putting out each member.
			
			for (var i = 0; i < keys.length; i++) {
				outlet(0, "append", keys[i]);
			}

		
		} else {
			// ketys is a string so just tell umenu about it.
			outlet(0, "append", keys);
		}
	
		outlet(1, "dictionary", devDict.name);		
	}
}
