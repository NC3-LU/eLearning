    function toggleInfo(card) {
        if (card.querySelector(".plot") && document.getElementById("plot-container")){
            const plot = card.querySelector(".plot").innerHTML;
            const plotContainer = document.getElementById("plot-container");
            plotContainer.innerHTML = plot;
        }

        if (card.querySelector(".plot") && document.getElementById("plot-container")){
            const plot = card.querySelector(".plot").innerHTML;
            const plotContainer = document.getElementById("plot-container");
            plotContainer.innerHTML = plot;
        }

        if (card.querySelector(".objectives") && document.getElementById("objectives-container")){
            const objectives = card.querySelector(".objectives").innerHTML;
            const objectivesContainer = document.getElementById("objectives-container");
            objectivesContainer.innerHTML = objectives;
        }

        if (card.querySelector(".duration") && document.getElementById("duration-container")){
            const duration = card.querySelector(".duration").innerHTML;
            const durationContainer = document.getElementById("duration-container");
            durationContainer.innerHTML = duration;
        }

        if (card.querySelector(".complexity") && document.getElementById("complexity-container")){
            const complexity = card.querySelector(".complexity").innerHTML;
            const complexityContainer = document.getElementById("complexity-container");
            complexityContainer.innerHTML = complexity;
        }

        if (card.querySelector(".requirements") && document.getElementById("requirements-container")){
            const requirements = card.querySelector(".requirements").innerHTML;
            const requirementsContainer = document.getElementById("requirements-container");
            requirementsContainer.innerHTML = requirements;
        }
    }

    window.onload = function () {
        const firstCard = document.querySelector(".card");
        toggleInfo(firstCard);
    };
