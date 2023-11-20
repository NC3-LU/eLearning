$(function () {
	function updateConnector() {
	    const connectors = document.getElementsByClassName('connector');
		const leftDots = document.getElementsByClassName('left-dot');
		const rightDots = document.getElementsByClassName('right-dot');

		console.log("CONNECTOR", connectors, leftDots, rightDots);

		for (let i = 0; i < connectors.length; i++) {
			let rightDot = undefined;
			let leftDot = undefined;

			for (let y = 0; y < rightDots.length; y++) {
				console.log("BBB", rightDots[y].id, "right-dot-" + connectors[i].dataset.value);
				if (rightDots[y].id == "right-dot-" + connectors[i].dataset.value) {
					rightDot = rightDots[y];
					break;
				}
			}

			for (let y = 0; y < leftDots.length; y++) {
				if (leftDots[y].id == "left-dot-" + connectors[i].dataset.value) {
					leftDot = leftDots[y];
					break;
				}
			}

			console.log("DOTS", rightDot, leftDot);

			if (rightDot !== undefined && leftDot !== undefined) {
				const topPosition = Math.min(rightDot.offsetTop, leftDot.offsetTop);
			    const height = Math.abs(rightDot.offsetTop - leftDot.offsetTop) + rightDot.offsetHeight;

			    console.log("POS", leftDot.offsetTop, rightDot.offsetTop, leftDot.offsetLeft, rightDot.offsetLeft);
			    connectors[i].style.top = leftDot.offsetTop + 'px';
			    connectors[i].style.bottom = rightDot.offsetTop + 'px';
			    connectors[i].style.left = leftDot.offsetLeft + 'px';
			    connectors[i].style.right = rightDot.offsetLeft + 'px';
			}
		}
	}

	const connectors = document.getElementsByClassName('connector');
	const leftDots = document.getElementsByClassName('left-dot');
	const rightDots = document.getElementsByClassName('right-dot');

	console.log("BEGGGINNN", connectors, leftDots, rightDots);

	for (let i = 0; i < rightDots.length; i++) {
		console.log('AAA', rightDots[i]);
		rightDots[i].addEventListener('click', updateConnector);
	}

	for (let i = 0; i < leftDots.length; i++) {
		leftDots[i].addEventListener('click', updateConnector);
	}

	window.addEventListener('resize', updateConnector);
	updateConnector();
});
