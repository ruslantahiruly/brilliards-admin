// TABLE
var tableInstance;
// console.log(project);

$('.table-add').click(function () {
	tableInstance = tableGroup.clone();
	tableInstance.visible = true;
	tableInstance.position = view.center;

	tableInstance.strokeWidth = '2';
	tableInstance.strokeColor = 'black';
	tableInstance.onMouseDrag = function(event) {
		this.position += event.delta;
	}

	tableInstance.onClick = function(event) {
		if (this.strokeColor == 'black') {
			this.strokeColor = 'red';
		} else if (this.strokeColor == 'red') {
			this.strokeColor = 'black';
		}
	}
});

$('.hall-layout-input').change(function () {
	var number = $('.hall-layout-input').val();
	// console.log(number);
	// tableInstance.children[1].content = number;
	var children = project.activeLayer.children;
	for (var i = 0; i < children.length; i++) {
		var child = children[i];
		if (child.strokeColor == 'red') {
			child.children[1].content = number;
		}
	}
});

$('.table-delete').click(function () {
	var children = project.activeLayer.children;
	for (var i = 0; i < children.length; i++) {
		var child = children[i];
		if (child.strokeColor == 'red') {
			child.remove();
		}
	}
});

var table = new Path.Rectangle({
	point: [0, 0],
	size: [60, 100],
	radius: 10,
	fillColor: 'red',
	strokeColor: 'black',
	strokeWidth: '1',
});

var tableNumber = new PointText({
	point: table.position,
	content: '1',
	justification: 'center',
	fontSize: 20
});

var tableGroup = new Group([table, tableNumber]);
tableGroup.visible = false;

// tableGroup.onMouseDown = function(event) {
// 	tableInstance = this.clone();
//
// 	tableInstance.strokeWidth = '2';
// 	tableInstance.onMouseDrag = function(event) {
// 		this.position += event.delta;
// 	}
//
// 	tableInstance.children[1].onClick = function(event) {
// 		this.content = number;
// 		console.log("tableNumber!!!");
// 	}
// }

// WALL
var wall = new Path();
wall.strokeColor = 'black';

$('.draw-scheme').click(function () {
	if ( $('.draw-scheme').hasClass('active') ) {
		$(this).removeClass('active');
	} else {
		$(this).addClass('active');

	}
});

function onMouseDown(event) {
	if ( $('.draw-scheme').hasClass('active') ) {
		wall.add(event.point);
	}

}

// var wallInstance;
// wall.onMouseDown = function(event) {
// 	wallInstance = this.clone();
//
// 	wallInstance.strokeWidth = '2';
// 	wallInstance.onMouseDrag = function(event) {
// 		this.position += event.delta;
// 	}
// }

// var img = new Image();
// img.src = '/static/clubs/images/club_scheme.png';
// img.addEventListener("load", function() {
// 	project.activeLayer.drawImage(img, 0,0);
// }, false);

var raster = new Raster('club-scheme');
raster.position = view.center;

$('.save-scheme').click(function () {
	var img = canvas.toDataURL();
	console.log('yes');
	$.ajax({
		type: 'POST',
		url: '/club-scheme/',
		data: {clubScheme: img}
	}).done(function () {
		console.log('Scheme!!!');
	});
});
