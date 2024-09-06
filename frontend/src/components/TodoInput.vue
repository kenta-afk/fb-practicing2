<script setup>
import { ref } from "vue";
import axios from "axios";
//import { statuses } from "../const/status";

const input = ref("");
const inputDate = ref("");
const isErrMsg = ref(false);

async function onSubmitForm(event) {
    event.preventDefault();
    
    if (input.value === "" || inputDate.value === "") {
        event.preventDefault();
        isErrMsg.value = true;
        
        return;
    }

    const newItem = {
        name: input.value,
        deadline: inputDate.value, 
    };

    try {
        await axios.post("http://localhost:8000/api/TodoInputView/items/",  newItem );
        console.log("Item created successfully");
    } catch (error) {
        console.error("Error creating item:", error);
    }
    location.reload();

}
</script>

<template>
    <div>
        <p v-if="isErrMsg">タスク・期限を両方入力してください。</p>
        <form @submit="onSubmitForm">
            <label>やること<input type="text" v-model="input" /></label>
            <label>期限<input type="date" v-model="inputDate" /></label>
            <input type="submit" value="登録！" />
        </form>
    </div>
</template>
