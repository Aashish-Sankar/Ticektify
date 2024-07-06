import { createStore } from 'vuex';

const store = createStore({
  state() {
    return {
      searchResults: [],
    };
  },
  mutations: {
    setSearchResults(state, results) {
      state.searchResults = results;
    },
  },
});

export default store;
