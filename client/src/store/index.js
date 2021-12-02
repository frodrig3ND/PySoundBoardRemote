import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';

/* eslint no-shadow: ["error", { "allow": ["state"] }] */

Vue.use(Vuex);

const state = {
  buttons: [],
};

const getters = {
  buttonList: (state) => (state.buttons),
};

const actions = {
  async fetchButtons({ commit }) {
    const response = await axios.get('http://192.168.1.181:8000/buttons');
    commit('setButtons', response.data);
  },
  async addButton({ commit }, button) {
    const response = await axios.post('http://192.168.1.181:8000/buttons', button);
    commit('addNewButton', response.data);
  },
  async editButton({ commit }, payload) {
    const response = await axios.put(`http://192.168.1.181:8000/buttons/${payload.id}`, payload.data);
    commit('modButton', response.data);
  },
  async deleteButton({ commit }, id) {
    await axios.delete(`http://192.168.1.181:8000/buttons/${id}`);
    commit('removeButton', id);
  },
};

const mutations = {
  setButtons: (state, buttons) => {
    state.buttons = buttons;
  },
  addNewButton: (state, button) => { state.buttons.unshift(button); },
  modButton(state, button) {
    const index = state.buttons.findIndex((item) => item.id === button.id);
    state.buttons[index].name = button.name;
    state.buttons[index].num = button.num;
    state.buttons[index].order = button.order;
  },
  removeButton(state, id) {
    const ibutton = state.buttons.filter((button) => button.id !== id);
    state.buttons.splice(ibutton, 1);
  },
};

export default new Vuex.Store({
  state,
  getters,
  actions,
  mutations,
});
