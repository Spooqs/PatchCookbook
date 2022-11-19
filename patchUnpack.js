autowatch = 1
inlets = 1
outlets = 9

setoutletassist(0, "osc_a text")
setoutletassist(1, "osc_b text")
setoutletassist(2, "osc_c text")
setoutletassist(3, "osc_d text")
setoutletassist(4, "main text")
setoutletassist(5, "filter text")
setoutletassist(6, "lfo text")
setoutletassist(7, "pitch text")
setoutletassist(8, "dictionary")

var patch_name = null;
var dictionary_name = null;

function patch(name) {
	post("patch seen on inlet " + inlet + "\n");
	patch_name = name;
	bang();
}

function dictionary(name) {
	post("dictionary seen on inlet " + inlet + "\n");
	dictionary_name = name;
	bang();
}

function bang() {
	
	if (patch_name && dictionary_name) {
		post("UNPACK \n");
		post("running with dict = `" + dictionary_name + "`\n");
		post("running with patch = `" + patch_name + "`\n");
		
		var catDict = new Dict(dictionary_name);
		
		var patchDict = catDict.get(patch_name);
		
		if (! patchDict) {
			post(patch_name + " not found in patches file\n");
			return null;
		}
		
		post("patchDict is a " + catDict.gettype(target_category_name) + "\n")
		
		var recipeDict = patchDict.get("recipe")
		
		if (! recipeDict) {
			post(" could not find the recipe in the path " + path_name + "\n");
			return null;
		}
		
		post("recipeDict is a " + patchDict.gettype(target_category_name) + "\n");
		
		outlet(0, "text", recipeDict.get("osc_a"));
		outlet(1, "text", recipeDict.get("osc_b"));
		outlet(2, "text", recipeDict.get("osc_c"));
		outlet(3, "text", recipeDict.get("osc_d"));
		outlet(4, "text", recipeDict.get("main"));	
		outlet(5, "text", recipeDict.get("filter"));	
		outlet(6, "text", recipeDict.get("lfo"));	
		outlet(7, "text", recipeDict.get("pitch"));
		
		outlet(8, "dictionary", patchDict.name);
		
		
		
	}
	
}