$(function () {
	$(".draggable-item").draggable({
		revert: "invalid",
	});

	$(".droppable").droppable({
		accept: ".draggable-item",
		drop: function (event, ui) {
			const clone = $(ui.helper).clone()
			$(this).append(clone);
			$(ui.helper).remove();
			clone.css("left", "unset");
			clone.css("top", "unset");
		}
	});
});
