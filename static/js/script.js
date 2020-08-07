function global_start() {
	var btn = document.getElementById("start");
	var url;
	if (btn.className == "btn btn-success")
	{
		url = global_start_url
		btn.className = "btn btn-danger";
		btn.innerHTML = '<span class="fa fa-stop" aria-hidden="true" id="start_span"></span> Stop All';
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

function delete_task(index) {
	$.ajax({
		type: 'POST',
		url: "/delete_task",
		data: {'index': index},
		success: function (data) {
		}
	});
}

function new_task() {
	$("#task").modal("show");
	document.getElementById("task-title").innerText = "New Task";
	document.getElementById("task-ok").innerText = "Add Task";
	document.getElementById("task_name").value = "";
	document.getElementById("task_timeout").value = "";
	document.getElementById("task_command").value = "";
}

var now_index = null;
function edit_task(index, name, cmd, timeout) {
	$("#task").modal("show");
	document.getElementById("task-title").innerText = "Edit Task";
	document.getElementById("task-ok").innerText = "Save Changes";
	document.getElementById("task_name").value = name;
	document.getElementById("task_timeout").value = timeout;
	document.getElementById("task_command").value = cmd;
	now_index = index
}

function save_change() {
	var name = document.getElementById("task_name").value;
	var timeout = document.getElementById("task_timeout").value;
	var command = document.getElementById("task_command").value;
	
	if (document.getElementById("task-title").innerText == "Edit Task")
	{
		$.ajax({
			type: 'POST',
			url: "/edit_task",
			data: {'index': now_index, 'name': name, 'timeout': timeout, 'cmd': command},
			success: function (data) {
			}
		});
	}
	else
	{
		$.ajax({
			type: 'POST',
			url: "/add_task",
			data: {'name': name, 'timeout': timeout, 'cmd': command},
			success: function (data) {
			}
		});
	}
}

function show_log(index) {
	$("#log").modal("show");
	$.ajax({
		type: 'POST',
		url: "/get_log",
		data: {'index': index},
		success: function (data) {
			document.getElementById('log_content').value = data
		}
	});
}

setInterval(get_tasks, 300);
function get_tasks() {
	$.ajax({
		type: 'GET',
		url: "/get_tasks",
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