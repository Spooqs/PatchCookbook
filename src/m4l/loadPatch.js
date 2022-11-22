autowatch = 1
inlets = 1
outlets = 2

var target_category_name = null;
var dictionary_name = null;


function category(name) {
	post("category seen on inlet " + inlet + "\n");
	target_category_name = name;
	bang();
}

function dictionary(name) {
	post("dictionary seen on inlet " + inlet + "\n");
	dictionary_name = name;
	bang();
}

function bang() {
	
	if (target_category_name && dictionary_name) {
		post("LOADPATCH \n");
		post("running with dict = `" + dictionary_name + "`\n");
		post("running with category = `" + target_category_name + "`\n");
	
		var devDict = new Dict(dictionary_name);
	
	
		var catDict = devDict.get(target_category_name);
		
		if (! catDict) {
			post(target_category_name + " not found in patches file\n");
			return null;
		}
		
		post("catDict is a " + devDict.gettype(target_category_name) + "\n")
			
	
		keys = catDict.getkeys()
		
		if ( keys === null || keys.length == 0) {
			post("No patches found for " + target_category_name + "\n");
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
	
		outlet(1, "dictionary", catDict.name);		
	}
}
