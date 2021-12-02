<template>
<div>
    <div>
      <br>
      <b-form-checkbox
      id="checkbox-1"
      v-model="delStatus"
      name="checkbox-delete"
      switch
      >
      Allow Delete
      </b-form-checkbox>
      <hr>
      <b-container class="bv-example-row">
        <b-row cols="1" cols-sm="2" cols-md="4" cols-lg="6">
          <b-col class="p-1" v-for="button in buttonsAll" :key="button.id">
            <div class="h-100" style="min-height: 10vh">
              <b-button size="md" class="w-100 h-100" variant="primary" @click="onButtonSel(button)"
            @contextmenu="onBtnContext(button, $event)">
            {{button.name}}</b-button>
            </div>
          </b-col>
          <b-col class="p-1">
            <b-button class="w-100 h-100"
            variant="outline-success" @click="onReset" v-b-modal.create-btn-modal>+</b-button>
          </b-col>
        </b-row>
      </b-container>
    </div>
<!-- create button modal -->
    <b-modal ref="createBtnModal"
      id="create-btn-modal"
      title="Create new Button"
      hide-footer>
      <b-form @submit="onCreate" class="w-100">
        <b-form-group id="form-size-group"
                        label="Name:"
                        label-for="form-name-input">
          <b-form-input id="form-name-input"
                        type="text"
                        v-model="editBtnForm.name"
                        required
                        placeholder="">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-size-group"
                        label="Number:"
                        label-for="form-command-input">
          <b-form-input id="form-command-input"
                        type="number"
                        v-model="editBtnForm.num"
                        required
                        placeholder="">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-size-group"
                        label="Order:"
                        label-for="form-order-input">
          <b-form-input id="form-order-input"
                        type="number"
                        v-model="editBtnForm.order"
                        required
                        placeholder="">
          </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Edit</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
<!-- edit button modal -->
    <b-modal ref="editBtnModal"
      id="edit-btn-modal"
      title="Edit Button record"
      hide-footer>
      <b-form class="w-100" @submit="onEdit">
        <b-form-group id="form-size-group"
                        label="Name:"
                        label-for="form-name-input">
          <b-form-input id="form-name-input"
                        type="text"
                        v-model="editBtnForm.name"
                        required
                        placeholder="">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-size-group"
                        label="Number:"
                        label-for="form-command-input">
          <b-form-input id="form-command-input"
                        type="number"
                        v-model="editBtnForm.num"
                        required
                        placeholder="">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-size-group"
                        label="Order:"
                        label-for="form-order-input">
          <b-form-input id="form-order-input"
                        type="number"
                        v-model="editBtnForm.order"
                        required
                        placeholder="">
          </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Edit</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
<!-- delete modal -->
    <b-modal ref="confirmDelete"
          id="del-conf"
          :title= "editBtnForm.name"
          hide-footer>
    <b-button-group>
      <b-button type="submit" variant="danger" @click="onDel">Delete</b-button>
    </b-button-group>
  </b-modal>
</div>
</template>
<script>
export default {
  name: 'ButtonsAll',
  data() {
    return {
      delStatus: false,
      btnDelid: '',
      editBtnForm: {
        num: '',
        name: '',
        order: '',
      },
    };
  },
  computed: {
    buttonsAll() {
      return this.$store.state.buttons;
    },
  },
  methods: {
    sendMessage(message) {
      this.connection.send(message);
    },
    onButtonSel(btn) {
      console.log(btn);
      this.sendMessage(btn.num);
    },
    onBtnContext(btn, evt) {
      evt.preventDefault();
      this.editBtnForm.num = btn.num;
      this.editBtnForm.name = btn.name;
      this.editBtnForm.order = btn.order;
      if (this.delStatus === false) {
        this.btnSelid = btn.id;
        this.$bvModal.show('edit-btn-modal');
      } else {
        this.btnSelid = btn.id;
        this.$bvModal.show('del-conf');
      }
    },
    onReset() {
      this.editBtnForm = {
        num: '',
        name: '',
        order: '',
      };
    },
    onCreate(evt) {
      evt.preventDefault();
      this.$bvModal.hide('create-btn-modal');
      const payload = {
        order: this.editBtnForm.order,
        name: this.editBtnForm.name,
        num: this.editBtnForm.num,
      };
      this.$store.dispatch('addButton', payload);
    },
    onEdit(evt) {
      evt.preventDefault();
      this.$bvModal.hide('edit-btn-modal');
      const payload = {
        order: this.editBtnForm.order,
        name: this.editBtnForm.name,
        num: this.editBtnForm.num,
      };
      this.$store.dispatch('editButton', { id: this.btnSelid, data: payload });
      this.btnSelid = '';
      this.onReset();
    },
    onDel(evt) {
      evt.preventDefault();
      this.$bvModal.hide('del-conf');
      this.$store.dispatch('deleteButton', this.btnSelid);
      this.btnSelid = '';
    },
  },
  mounted() {
    this.$store.dispatch('fetchButtons');
    console.log('Starting connection to WebSocket Server');
    this.connection = new WebSocket('ws://192.168.1.181:8000/ws');
    this.connection.onmessage = function (event) {
      console.log(event);
    };

    this.connection.onopen = function (event) {
      console.log(event);
      console.log('Successfully connected to the echo websocket server...');
    };
  },
};
</script>
