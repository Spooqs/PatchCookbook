autowatch = 1;
outlets = 2;
setoutletassist(1, "patch list in umenu format");

function bang() {
    post("Hello, world!");

    var testDict = new Dict("keys.json");
    var patches = testDict.get("patches");
    post();
    
    patches.forEach(function(patch) {
        post(patch.get("name"));
        outlet(1, "append", patch.get("name"));
    });
}