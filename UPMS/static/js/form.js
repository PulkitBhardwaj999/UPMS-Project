document.addEventListener("DOMContentLoaded", () => {
    const csrf = Cookies.get('csrftoken');
    
    // FORM TITLE CHANGE
    document.querySelectorAll(".input-form-title").forEach(title => {
        title.addEventListener("input", function(){
            fetch(`edit_title`, {
                method: "POST",
                headers: {'X-CSRFToken': csrf},
                body: JSON.stringify({
                    "title": this.value
                })
            })
            document.title = `${this.value}`
            document.querySelectorAll(".input-form-title").forEach(ele => {
                ele.value = this.value;
                $('.form-title-h4').text(this.value);
            })
        })
    })

    // DESCRIPTION CHANGE
    document.querySelector("#input-form-description").addEventListener("input", function(){
        fetch('edit_description', {
            method: "POST",
            headers: {'X-CSRFToken': csrf},
            body: JSON.stringify({
                "description": this.value
            })
        })
    })

    // FORM DELETE
    document.querySelector("#delete-form-btn").addEventListener("click", e => {
        fetch('delete', {
            method: "DELETE",
            headers: {'X-CSRFToken': csrf}
        })
        .then(() => window.location = "/")
    })

    // AUTO ADJUST TEXTAREA LINES
    document.querySelectorAll(".textarea-adjust").forEach(tx => {
        tx.style.height = "auto";
        tx.style.height = (10 + tx.scrollHeight)+"px";
        tx.addEventListener('input', e => {
            tx.style.height = "auto";
            tx.style.height = (10 + tx.scrollHeight)+"px";
        })
    })
    
    // PUBLISH BUTTON
    document.querySelectorAll("#send-form-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            document.querySelector("#send-form").style.display = "block";
        })
        document.querySelector("#close-send-form").addEventListener("click", () => {
            document.querySelector("#send-form").style.display = "none";
        })
        window.onclick = e => {
            if(e.target == document.querySelector("#send-form")) document.querySelector("#send-form").style.display = "none";
        }
    })

    // COPY BUTTON ON PUBLISH
    document.querySelectorAll("[copy-btn]").forEach(btn => {
        btn.addEventListener("click", () => {
            var url = document.getElementById("copy-url");
            navigator.clipboard.writeText(url.value);
            document.querySelector("#send-form").style.display = "none";
        })
    })
    
    // POST REQUESTS
    const editQuestion = () => {
        document.querySelectorAll(".input-question").forEach(question => {
            question.addEventListener('input', function(){
                let question_type;
                let required;
                document.querySelectorAll(".input-question-type").forEach(qp => {
                    if(qp.dataset.id === this.dataset.id) question_type = qp.value
                })
                document.querySelectorAll('.required-checkbox').forEach(rc => {
                    if(rc.dataset.id === this.dataset.id) required = rc.checked;
                })
                fetch('edit_question', {
                    method: "POST",
                    headers: {'X-CSRFToken': csrf},
                    body: JSON.stringify({
                        id: this.dataset.id,
                        question: this.value,
                        question_type: question_type,
                        required: required
                    })
                })
                $(`.question-title-h4-${this.dataset.id}`).text(this.value);
            })
        })
    }
    editQuestion();
    
    const editRequire = () => {
        document.querySelectorAll(".required-checkbox").forEach(checkbox => {
            checkbox.addEventListener('input', function(){
                let question;
                let question_type;
                document.querySelectorAll(".input-question-type").forEach(qp => {
                    if(qp.dataset.id === this.dataset.id) question_type = qp.value
                })
                document.querySelectorAll('.input-question').forEach(q => {
                    if(q.dataset.id === this.dataset.id) question = q.value
                })
                fetch('edit_question', {
                    method: "POST",
                    headers: {'X-CSRFToken': csrf},
                    body: JSON.stringify({
                        id: this.dataset.id,
                        question: question,
                        question_type: question_type,
                        required: this.checked
                    })
                })
            })
        })
    }
    editRequire()
    
    const editChoice = () => {
        document.querySelectorAll(".edit-choice").forEach(choice => {
            choice.addEventListener("input", function(){
                fetch('edit_choice', {
                    method: "POST",
                    headers: {'X-CSRFToken': csrf},
                    body: JSON.stringify({
                        "id": this.dataset.id,
                        "choice": this.value
                    })
                })
            })
        })
    }
    editChoice()

    const removeOption = () => {
        document.querySelectorAll(".remove-option").forEach(ele => {
            ele.addEventListener("click",function(){
                fetch('remove_choice', {
                    method: "POST",
                    headers: {'X-CSRFToken': csrf},
                    body: JSON.stringify({
                        "id": this.dataset.id
                    })
                })
                .then(() => {
                    this.parentNode.parentNode.removeChild(this.parentNode)
                })
            })
        })
    }
    removeOption()

    // ADD CHOICE/CHECKBOX OPTION
    const addOption = () => {
        document.querySelectorAll(".add-option").forEach(question =>{
            question.addEventListener("click", function(){
                fetch('add_choice', {
                    method: "POST",
                    headers: {'X-CSRFToken': csrf},
                    body: JSON.stringify({
                        "question": this.dataset.question
                    })
                })
                .then(response => response.json())
                .then(result => {
                    let element = document.createElement("div");
                    element.classList.add('choice');
                    if(this.dataset.type === "multiple choice"){
                        element.innerHTML = `<input type="radio" id="${result["id"]}" disabled>
                        <label for="${result["id"]}">
                            <input type="text" value="${result["choice"]}" class="form-control edit-choice" data-id="${result["id"]}">
                        </label>
                        <span class="remove-option" title = "Remove" data-id="${result["id"]}"><i class="fa fa-trash" aria-hidden="true"></i></span>`;
                    }else if(this.dataset.type === "checkbox"){
                        element.innerHTML = `<input type="checkbox" id="${result["id"]}" disabled>
                        <label for="${result["id"]}">
                            <input type="text" value="${result["choice"]}" class="form-control edit-choice" data-id="${result["id"]}">
                        </label>
                        <span class="remove-option" title = "Remove" data-id="${result["id"]}"><i class="fa fa-trash" aria-hidden="true"></i></span>`;
                    }
                    document.querySelectorAll(".choices").forEach(choices => {
                        if(choices.dataset.id === this.dataset.question){
                            choices.insertBefore(element, choices.childNodes[choices.childNodes.length -2]);
                            editChoice()
                            removeOption()
                        }
                    });
                })
            })
        })
    }
    addOption()

    // ADD QUESTION
    document.querySelectorAll(".add-question").forEach(ele => {
        ele.addEventListener('click', () => {
            fetch('add_question', {
                method: "POST",
                headers: {'X-CSRFToken': csrf},
                body: JSON.stringify({})
            })
            .then(response => response.json())
            .then(result => {
                let ele = document.createElement('div')
                ele.classList.add('card-deck');
                ele.classList.add('mb-3');
                ele.classList.add('text-center');
                ele.classList.add('question-box');
                ele.classList.add('question');
                ele.setAttribute("data-id", result["question"].id)
                ele.innerHTML = `
                <div class="card mb-4 box-shadow">

                    <!-- Question add or remove -->
                    <div class="card-header">
                        <h4 style="display:inline-block; float:left;" class="my-0 question-title-h4-${result["question"].id} font-weight-normal">${result["question"].question}</h4>
                        <button type="button" style="margin-right: 1%; float:right;" id="delete-form-btn" class="btn delete-question btn-outline-danger" data-id="${result["question"].id}">Delete Question!</button>
                    </div>

                    <div class="card-body">
                        <div>

                            <!-- Question -->
                            <div class="form-group row">
                                <label for="inputQuestion-${result["question"].id}" class="col-sm-2 col-form-label">Question</label>
                                <div class="col-sm-10">
                                    <input type="text" data-id="${result["question"].id}" class="form-control question-title edit-on-click input-question" id="inputQuestion-${result["question"].id}" value="${result["question"].question}">
                                </div>
                            </div>
                            
                            <!-- Question type -->
                            <div class="form-group row">
                                <label for="questionTypeSelect-${result["question"].id}" class="col-sm-2 col-form-label">Question Type</label>
                                <div class="col-sm-10">
                                    <select class="form-control question-type-select input-question-type" data-id="${result["question"].id}" data-origin_type = "${result["question"].question_type}" id="questionTypeSelect-${result["question"].id}">
                                        <option value="short">Short answer</option>
                                        <option value="paragraph">Paragraph</option>
                                        <option value="multiple choice">Multiple choice</option>
                                        <option value="checkbox">Checkbox</option>
                                    </select>
                                </div>
                            </div>

                            <div class="form-group row" data-id="${result["question"].id}">

                                <label for="demoOf-${result["question"].id}" class="col-sm-2 col-form-label">Demo:</label>

                                <div class="col-sm-10 answers type-short" data-id="${result["question"].id}">
                                    <input type="text" class="form-control short-answer" id="demoOf-${result["question"].id}" placeholder="Short answer type question" disabled>
                                </div>

                            </div>


                            <!-- Is question required? -->
                            <div class="form-group row choice-option">
                                <label for="required-${result["question"].id}" class="col-sm-2 col-form-label required">Required:</label>
                                <div class="col-sm-10">
                                    <input type="checkbox" class="required-checkbox" id="required-${result["question"].id}" data-id="${result["question"].id}" checked>
                                </div>
                            </div>

                        </div>
                    </div>
                </div>
                `;

                document.querySelector(".container").appendChild(ele);
                editChoice()
                removeOption()
                changeType()
                editQuestion()
                editRequire()
                addOption()
                deleteQuestion()
            })
        })        
    });

    // DELETE QUESTION
    const deleteQuestion = () => {
        document.querySelectorAll(".delete-question").forEach(question => {
            question.addEventListener("click", function(){
                fetch(`delete_question/${this.dataset.id}`, {
                    method: "DELETE",
                    headers: {
                        'X-CSRFToken': csrf
                    },
                })
                .then(() => {
                    document.querySelectorAll(".question").forEach(q =>{
                        if(q.dataset.id === this.dataset.id){
                            q.parentNode.removeChild(q)
                        }
                    })
                })
            })
        })
    }
    deleteQuestion()

    // QUESTION TYPE CHANGE
    const changeType = () => {
        document.querySelectorAll(".input-question-type").forEach(ele => {
            ele.addEventListener('input', function(){
                let required;
                let question;

                // GETTING REQUIRED CHECKBOX VALUE OF QUESTION
                document.querySelectorAll('.required-checkbox').forEach(rc => {
                    if(rc.dataset.id === this.dataset.id) {
                        required = rc.checked;
                    }
                })

                // GETTING QUESTION VALUE OF QUESTION
                document.querySelectorAll('.input-question').forEach(q => {
                    if(q.dataset.id === this.dataset.id) {
                        question = q.value;
                    }
                })

                fetch('edit_question', {
                    method: "POST",
                    headers: {
                        'X-CSRFToken': csrf
                    },
                    body: JSON.stringify({
                        id: this.dataset.id,
                        question: question,
                        question_type: this.value,
                        required: required
                    })
                })

                if(this.dataset.origin_type === "multiple choice" || this.dataset.origin_type === "checkbox") {
                    // DONE
                    document.querySelectorAll(".choices").forEach(choicesElement => {
                        if(choicesElement.dataset.id === this.dataset.id) {
                            if(this.value === "multiple choice" || this.value === "checkbox") {
                                fetch(`get_choice/${this.dataset.id}`, {
                                    method: "GET"
                                })
                                .then(response => response.json())
                                .then(result => {
                                    let ele = document.createElement("div");
                                    ele.classList.add('col-sm-10');
                                    ele.classList.add('choices');
                                    ele.setAttribute("data-id", result["question_id"])
                                    let choices = '';
                                    if(this.value === "multiple choice"){
                                        for(let i in result["choices"]) {
                                            if(i) { 
                                                choices += `
                                                <div class="choice">
                                                    <input type="radio" id="${result["choices"][i].id}" disabled>
                                                    <label for="${result["choices"][i].id}">
                                                        <input type="text" value="${result["choices"][i].choice}" class="form-control edit-choice" data-id="${result["choices"][i].id}">
                                                    </label>
                                                    <span class="remove-option" title="Remove" data-id="${result["choices"][i].id}"><i class="fa fa-trash" aria-hidden="true"></i></span>
                                                </div>
                                                `
                                            }
                                        }
                                    } else if (this.value === "checkbox"){
                                        for(let i in result["choices"]) {
                                            if(i) {
                                                choices += `
                                                <div class="choice">
                                                    <input type="checkbox" id="${result["choices"][i].id}" disabled>
                                                    <label for="${result["choices"][i].id}">
                                                        <input type="text" value="${result["choices"][i].choice}" class="form-control edit-choice" data-id="${result["choices"][i].id}">
                                                    </label>
                                                    <span class="remove-option" title="Remove" data-id="${result["choices"][i].id}"><i class="fa fa-trash" aria-hidden="true"></i></span>
                                                </div>
                                                `
                                            }
                                        }
                                    }
                                    ele.innerHTML = `${choices}
                                    <div class="choice">
                                        <button type="button" style="margin-right: 1%;" class="btn add-option btn-warning" id="add-option" data-question="${result["question_id"]}"
                                        data-type = "${this.value}">Add Choice!</button>
                                    </div>`;
                                    choicesElement.parentNode.replaceChild(ele, choicesElement);
                                    editChoice()
                                    removeOption()
                                    changeType()
                                    editQuestion()
                                    editRequire()
                                    addOption()
                                    deleteQuestion()
                                })
                            } else {
                                if(this.value === "short"){
                                    choicesElement.parentNode.removeChild(choicesElement)
                                    let ele = document.createElement("div");
                                    ele.classList.add('col-sm-10');
                                    ele.classList.add('answers');
                                    ele.classList.add('type-short');
                                    ele.classList.add('question-box');
                                    ele.classList.add('question');
                                    ele.setAttribute("data-id", this.dataset.id)
                                    ele.innerHTML = `<input type="text" class="form-control short-answer" id="demoOf-${this.dataset.id}"" placeholder="Short answer type question" disabled>`
                                    document.querySelector(`.row[data-id="${this.dataset.id}"]`).append(ele);
                                } else if(this.value === "paragraph") {
                                    choicesElement.parentNode.removeChild(choicesElement)
                                    let ele = document.createElement("div");
                                    ele.classList.add('col-sm-10');
                                    ele.classList.add('answers');
                                    ele.classList.add('type-short');
                                    ele.classList.add('question-box');
                                    ele.classList.add('question');
                                    ele.setAttribute("data-id", this.dataset.id)
                                    ele.innerHTML = `<textarea class="form-control long-answer" disabled placeholder="Long answer type question" rows="3"></textarea>`
                                    document.querySelector(`.row[data-id="${this.dataset.id}"]`).append(ele);
                                }
                            }
                        }
                    })
                } else {
                    // REMOVE ANSWER BOX
                    document.querySelectorAll(`.answers[data-id="${this.dataset.id}"]`).forEach(answer => {
                        if(answer.dataset.id === this.dataset.id){
                            answer.parentNode.removeChild(answer)
                        }
                    })
                    document.querySelectorAll(`.question-box[data-id="${this.dataset.id}"]`).forEach(question => {
                        // IF BUTTON IS CHOICE/CHECKBOX
                        if((this.value === "multiple choice" || this.value === "checkbox") && question.dataset.id === this.dataset.id) {
                            fetch(`get_choice/${this.dataset.id}`, {
                                method: "GET"
                            })
                            .then(response => response.json())
                            .then(result => {             
                                let ele = document.createElement("div");
                                ele.classList.add('col-sm-10');
                                ele.classList.add('choices');
                                ele.setAttribute("data-id", this.dataset.id)
                                let choices = '';
                                if(this.value === "multiple choice"){
                                    for(let i in result["choices"]){
                                        if(i){ 
                                            choices += `
                                            <div class="choice">
                                                <input type="radio" id="${result["choices"][i].id}" disabled>
                                                <label for="${result["choices"][i].id}">
                                                    <input type="text" value="${result["choices"][i].choice}" class="form-control edit-choice" data-id="${result["choices"][i].id}">
                                                </label>
                                                <span class="remove-option" title = "Remove" data-id="${result["choices"][i].id}"><i class="fa fa-trash" aria-hidden="true"></i></span>
                                            </div>
                                            `
                                        }
                                    }
                                } else if(this.value === "checkbox") {
                                    for(let i in result["choices"]) {
                                        if(i) {
                                            choices += `
                                            <div class="choice">
                                                <input type="checkbox" id="${result["choices"][i].id}" disabled>
                                                <label for="${result["choices"][i].id}">
                                                    <input type="text" data-id="${result["choices"][i].id}" class="form-control edit-choice" value="${result["choices"][i].choice}">
                                                </label>
                                                <span class="remove-option" title="Remove" data-id="${result["choices"][i].id}"><i class="fa fa-trash" aria-hidden="true"></i></span>
                                            </div>
                                            `
                                        }
                                    }
                                }
                                ele.innerHTML = `${choices}
                                    <div class="choice">
                                        <button type="button" style="margin-right: 1%;" class="btn add-option btn-warning" id="add-option" data-question="${result["question_id"]}"
                                        data-type = "${this.value}">Add Choice!</button>
                                    </div>
                                `;
                                document.querySelector(`.row[data-id="${this.dataset.id}"]`).append(ele);
                                editChoice()
                                removeOption()
                                changeType()
                                editQuestion()
                                editRequire()
                                addOption()
                                deleteQuestion()
                            })
                        } else {
                            // DONE
                            if(this.value === "short"){
                                let ele = document.createElement("div");
                                ele.classList.add('col-sm-10');
                                ele.classList.add('answers');
                                ele.classList.add('type-short');
                                ele.classList.add('question-box');
                                ele.classList.add('question');
                                ele.setAttribute("data-id", this.dataset.id)
                                ele.innerHTML = `<input type="text" class="form-control short-answer" id="demoOf-${this.dataset.id}"" placeholder="Short answer type question" disabled>`
                                document.querySelector(`.row[data-id="${this.dataset.id}"]`).append(ele);
                            } else if(this.value === "paragraph") {
                                let ele = document.createElement("div");
                                ele.classList.add('col-sm-10');
                                ele.classList.add('answers');
                                ele.classList.add('type-short');
                                ele.classList.add('question-box');
                                ele.classList.add('question');
                                ele.setAttribute("data-id", this.dataset.id)
                                ele.innerHTML = `<textarea class="form-control long-answer" disabled placeholder="Long answer type question" rows="3"></textarea>`
                                document.querySelector(`.row[data-id="${this.dataset.id}"]`).append(ele);
                            }
                        }
                    })
                }
                this.setAttribute("data-origin_type", this.value);
            })
        })
    }
    changeType()
})