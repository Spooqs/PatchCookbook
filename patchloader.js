autowatch = 1;
outlets = 2;
setoutletassist(1, "patch list in umenu format");

function bang() {
    post("Hello, world!");

    var bassPatches = new Dict("bass.json");
	var leadPatches = new Dict("lead.json");
	var keysPatches = new Dict("keys.json");
	var drumPatches = new Dict("drum.json");
	var miscPatches = new Dict("misc.json");
    var patches = leadPatches.get("patches");
    post();
    
    patches.forEach(function(patch) {
        post(patch.get("name"));
        outlet(1, "append", patch.get("name"));
    });
}