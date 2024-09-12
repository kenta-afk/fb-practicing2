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
let inputDeadline = ref(); 


let isErrMsg = ref(false);

let isShowModal = ref(false);
let deleteItemId = '';
let updateItemId = '';

function onEdit(id) {
    const item = items.value.find(item => item.item_id === id);

    if (item) {
        inputContent.value = item.name;
        inputDeadline.value = item.deadline;
        item.onEdit = true;
        updateItemId = id;  // 更新対象のIDを保存
    }
}

async function onUpdate(id) {
    if (inputContent.value == "" || inputDeadline.value == "") {
        isErrMsg.value = true;
        return;
    }

    // 更新リクエストを送信
    try {
        const updatedItem = {
            name: inputContent.value,
            deadline: inputDeadline.value,
        };

        await axios.put(`http://localhost:8000/api/TodoInputView/items/${id}`, updatedItem);
        
        // ローカルのitemsを更新
        const index = items.value.findIndex(item => item.item_id === id);
        items.value[index].name = updatedItem.name;
        items.value[index].deadline = updatedItem.deadline;
        items.value[index].onEdit = false;

        console.log("Item updated successfully");
    } catch (error) {
        console.error("Failed to update item:", error);
    }
}

function showDeleteModal(id) {
    console.log(id);
    isShowModal.value = true;
    deleteItemId = id;
}

async function onDeleteItem() {
    try {
        // DELETEリクエストを送信してデータを削除
        await axios.delete(`http://localhost:8000/api/TodoInputView/items/${deleteItemId}`);
        
        // ローカルのitemsから削除
        const index = items.value.findIndex(item => item.item_id === deleteItemId);
        items.value.splice(index, 1);
        isShowModal.value = false;

        console.log("Item deleted successfully");
    } catch (error) {
        console.error("Failed to delete item:", error);
    }
    
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
            <tr v-for="(item, index) in items" :key="item.item_id">
                <td>{{ item.item_id }}</td>
                <td>
                    <span v-if="!item.onEdit">{{ item.name }}</span> <!-- nameを表示 -->
                    <input v-else v-model="inputContent" type="text" />
                </td>
                <td>
                    <span v-if="!item.onEdit">{{ item.deadline }}</span> <!-- 期限を表示 -->
                    <input v-else v-model="inputDeadline" type="date" />
                </td>
                <td>
                    <button v-if="!item.onEdit" @click="onEdit(item.item_id)">編集</button>
                    <button v-else @click="onUpdate(item.item_id)">完了</button>
                </td>
                <td><button @click="showDeleteModal(item.item_id)">削除</button></td>
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
