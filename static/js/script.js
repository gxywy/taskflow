function global_start() {
	var btn = document.getElementById("start");
	var url;
	if (btn.className == "btn btn-success")
	{
		url = global_start_url
		btn.className = "btn btn-danger";
		btn.innerHTML = '<span class="fa fa-stop" aria-hidden="true" id="start_span"></span> Stop';
	}
	else
	{
		url = global_stop_url
		btn.className = "btn btn-success";
		btn.innerHTML = '<span class="fa fa-play" aria-hidden="true" id="start_span"></span> Start';
	}
	$.ajax({
		type: 'GET',
		url: url,
		success: function () {
		}
	});
}

function tasklists() {
	$("#load").modal("show");
	$.ajax({
		type: 'GET',
		url: get_lists_url,
		success: function (data) {
			var html;
			for (i in data.files) {
				html += '<option>' + data.files[i] + '</option>'
			}
			document.getElementById("loadSelect").innerHTML = html;
		}
	});
}

function save_list() {
	$("#backup").modal("show");
}

function new_task() {
	$("#task").modal("show");
	document.getElementById("task-title").innerText = "New Task";
	document.getElementById("task-ok").innerText = "Add Task";
	document.getElementById("task_name").value = "";
	document.getElementById("task_timeout").value = "";
	document.getElementById("task_command").value = "";
}

function delete_task(index) {
	$.ajax({
		type: 'POST',
		url: delete_task_url,
		data: {'index': index},
		success: function (data) {
		}
	});
}

function order_up(index) {
	$.ajax({
		type: 'POST',
		url: order_up_url,
		data: {'index': index},
		success: function (data) {
		}
	});
}

function order_down(index) {
	$.ajax({
		type: 'POST',
		url: order_down_url,
		data: {'index': index},
		success: function (data) {
		}
	});
}
var now_index = null;
function edit_task(index) {
	$("#task").modal("show");
	now_index = index
	$.ajax({
		type: 'POST',
		url: get_task_url,
		data: {'index': now_index},
		success: function (data) {
			document.getElementById("task-title").innerText = "Edit Task";
			document.getElementById("task-ok").innerText = "Save Changes";
			document.getElementById("task_name").value = data.name;
			document.getElementById("task_timeout").value = data.timeout;
			document.getElementById("task_command").value = data.cmd;
		}
	});
}

function show_log(index) {
	$("#log").modal("show");
	$.ajax({
		type: 'POST',
		url: get_log_url,
		data: {'index': index},
		success: function (data) {
			document.getElementById('log_content').value = data;
		}
	});
}

setInterval(get_tasks, 500);
function get_tasks() {
	$.ajax({
		type: 'GET',
		url: get_tasks_url,
		success: function (data) {
			if (data.search("running") == -1)
			{
				var btn = document.getElementById("start");
				btn.className = "btn btn-success";
				btn.innerHTML = '<span class="fa fa-play" aria-hidden="true" id="start_span"></span> Start';
			}
			document.getElementById('dashboard').innerHTML = data
		}
	});
}