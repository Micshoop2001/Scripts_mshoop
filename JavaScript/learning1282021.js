//this is the test got this off of presentation
require(["esri/Map", "esri/views/MapView"], function (
	Map,
	MapView
	) {

	const map = new Map({
		basemap: "gray-vector"
	});
	view = new MapView({
		container: "viewDiv",
		map: map,
		zoom: 10,
		center: [-87.68914, 41.85978] //longitude, latitude
	});
});