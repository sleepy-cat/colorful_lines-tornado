$(document).ready(function(){

test("creation test", function () {
    expect(6);
    
    // Empty
    var g = new Graph([], null);    
    ok(g, "g created");
    ok(g.graph);
    
    // A small graph:
    //
    var sfunc = function (v) {
        var o = {}
        o[2] = [4, 20];
        o[20] = [2];
        o[4] = [3];
        o[1] = [2];
        o[3] = [2];
        
        if (o.hasOwnProperty(v)) {
            return o[v];
        } 
        return [];
    }
    
    var g = new Graph([1, 2, 3, 4, 20], sfunc);
    same(g.find_path(3, 1), null);
    g.clear(); same(g.find_path(2, 20), [20]);
    g.clear(); same(g.find_path(1, 20), [2, 20]);
    g.clear(); same(g.find_path(1, 3), [2, 4, 3]);
});


});
