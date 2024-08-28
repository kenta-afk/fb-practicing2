<script setup>
import { ref, onMounted } from "vue";
import axios from "axios"; // axiosを利用してAPIリクエストを送信

let items = ref([]);

onMounted(async () => {
    try {
        const response = await axios.get("http://localhost:8000/api/TodoInputView/items/");
        console.log(response.data);
        items.value = response.data;
    } catch (error) {
        console.error("Failed to fetch items:", error);
    }
});

let inputContent = ref();
let inputDeadline = ref(); // limitをdeadlineに変更
let inputState = ref();

let isErrMsg = ref(false);

let isShowModal = ref(false);
let deleteItemId = '';

function onEdit(id) {
    const item = items.value.find(item => item.id === id);
    inputContent.value = item.name;
    inputDeadline.value = item.deadline; // limitをdeadlineに変更
    inputState.value = item.state;
    item.onEdit = true;
}

function onUpdate(id) {
    if (inputContent.value == "" || inputDeadline.value == "") {
        isErrMsg.value = true;
        return;
    }

    const updatedItem = {
        id: id,
        name: inputContent.value,
        deadline: inputDeadline.value, 
        state: inputState.value,
        onEdit: false,
    };

    const index = items.value.findIndex(item => item.id === id);
    items.value.splice(index, 1, updatedItem);
}

function showDeleteModal(id) {
    isShowModal.value = true;
    deleteItemId = id;
}

function onDeleteItem() {
    const index = items.value.findIndex(item => item.id === deleteItemId);
    items.value.splice(index, 1);
    isShowModal.value = false;
}

function dropDeleteModal() {
    isShowModal.value = false;
}
</script>

<template>
    <p v-if="isErrMsg">タスク・期限を両方入力してください。</p>
    <div>
        <table>
            <tr>
                <th class="th-id">ID</th>
                <th class="th-value">やること</th>
                <th class="th-limit">期限</th>
                <th class="th-edit">編集</th>
                <th class="th-delete">削除</th>
            </tr>
            <tr v-for="item in items" :key="item.id">
                <td>{{ item.id }}</td>
                <td>
                    <span v-if="!item.onEdit">{{ item.name }}</span> <!-- nameを表示 -->
                    <input v-else v-model="inputContent" type="text" />
                </td>
                <td>
                    <span v-if="!item.onEdit">{{ item.deadline }}</span> <!-- 期限を表示 -->
                    <input v-else v-model="inputDeadline" type="date" />
                </td>
                <td>
                    <button v-if="!item.onEdit" @click="onEdit(item.id)">編集</button>
                    <button v-else @click="onUpdate(item.id)">完了</button>
                </td>
                <td><button @click="showDeleteModal(item.id)">削除</button></td>
            </tr>
        </table>
    </div>
    <div v-if="isShowModal" class="modal">
        <div class="modal-content">
            <p>削除してもよろしいですか？</p>
            <button @click="onDeleteItem">はい</button>
            <button @click="dropDeleteModal">キャンセル</button>
        </div>
    </div>
</template>
