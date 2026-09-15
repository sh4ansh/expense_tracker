// =====================================================
// DATE AUTO-FILL
// =====================================================

const dateInput = document.querySelector(
    'input[name="expense_date"]'
);

if (dateInput) {

    const today = new Date();

    const year = today.getFullYear();

    const month = String(
        today.getMonth() + 1
    ).padStart(2, "0");

    const day = String(
        today.getDate()
    ).padStart(2, "0");

    // Only set today's date when the form is empty.
    if (!dateInput.value) {

        dateInput.value =
            `${year}-${month}-${day}`;

    }

}



// =====================================================
// CALCULATOR
// =====================================================

const calculatorButton =
    document.getElementById("calculatorButton");

const calculator =
    document.getElementById("calculator");

const closeCalculator =
    document.getElementById("closeCalculator");

const display =
    document.getElementById("calcDisplay");

const clearCalculator =
    document.getElementById("clearCalculator");

const calculateButton =
    document.getElementById("calculate");



if (
    calculatorButton &&
    calculator &&
    display
) {

    // Open calculator

    calculatorButton.addEventListener(
        "click",
        function () {

            calculator.classList.toggle("show");

        }
    );


    // Close calculator

    closeCalculator.addEventListener(
        "click",
        function () {

            calculator.classList.remove("show");

        }
    );


    // Number/operator buttons

    const buttons =
        calculator.querySelectorAll(
            "[data-value]"
        );


    buttons.forEach(
        function (button) {

            button.addEventListener(
                "click",
                function () {

                    const value =
                        button.dataset.value;


                    if (display.value === "0") {

                        display.value = value;

                    } else {

                        display.value += value;

                    }

                }
            );

        }
    );


    // Calculate

    calculateButton.addEventListener(
        "click",
        function () {

            try {

                const expression =
                    display.value;


                // Only allow calculator characters

                if (
                    !/^[0-9+\-*/. ]+$/.test(
                        expression
                    )
                ) {

                    display.value = "Error";

                    return;

                }


                const result =
                    Function(
                        `"use strict"; return (${expression})`
                    )();


                if (
                    !Number.isFinite(result)
                ) {

                    display.value = "Error";

                    return;

                }


                display.value =
                    Number(result.toFixed(10));


            } catch {

                display.value = "Error";

            }

        }
    );


    // Clear

    clearCalculator.addEventListener(
        "click",
        function () {

            display.value = "0";

        }
    );

}