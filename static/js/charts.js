// Neven Recchia 27968018
// http://adilmoujahid.com/posts/2015/01/interactive-data-visualization-d3-dc-python-mongodb/

d3.queue()
	.defer(d3.json, "http://0.0.0.0:5000/DinoFunFriday")
	.await(makeGraphs);

function makeGraphs(error, projectsJson){

	// load data
	var fridaymovement = projectsJson;
	var timeFormat = d3.time.format("%Y-%m-%d %H:%M:%S");
	fridaymovement.forEach(function(d){
		d["Timestamp"] = timeFormat.parse(d["Timestamp"]);
		d["id"] = +d["id"];
		d["X"] = +d["X"];
		d["Y"] = +d["Y"];
		d["chkcount"] = +d["chkcount"];
		d["gsize"] = +d["gsize"];
		d["ngroup"] = +d["ngroup"];
	});

	// crossfilter dimensions and groups
	var ndx = crossfilter(fridaymovement);
	var all = ndx.groupAll();

	// // dimension by hour
	// var hourDimension = fb.dimension(function (d){
	// 	return d.hour;
	// });
	// var hourGroup = hourDimension.group();

	// dimension
	var groupSizeDimension = ndx.dimension(function(d){
		return d["gsize"];
	});
	var sumGroup = groupSizeDimension.group().reduceSum(function(d){
		return d["ngroup"];
	});

	// create chart objects
	var nGroupSizeChart = dc.barChart("#group-size-bar-chart");


	// group size bar chart
	postHourChart
        .width(1000)
        .height(300)
        .brushOn(false)
        .dimension(groupSizeDimension)
        .group(sumGroup)
        .elasticY(true)
        .centerBar(false)
        .gap(0)
        .x(d3.scale.ordinal())
        .xUnits(dc.units.ordinal)
        .renderHorizontalGridLines(true)
        .renderVerticalGridLines(true)
        .title(function (d){
            return "Group Size: " + d["gsize"] + "\n" +
                "Number of Groups: " + d["ngroup"];
        })
        .xAxisLabel('Group Size')
        .yAxisLabel('Number of Groups');

    // render
    dc.renderAll();

};