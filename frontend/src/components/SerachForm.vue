<template>
    <form
      class="d-flex"
      role="search"
    >
      <input
        class="form-control me-2"
        type="search"
        placeholder="Search"
        aria-label="Search"
        name="searched"
        v-model="searchTerm"
      />
      <button
        class="btn btn-outline-secondary"
        type="submit"
        @click.prevent="search"
      >
        Search
      </button>
    </form>
  </template>
  
  <script>
  import { mapMutations } from 'vuex';
  
  export default {
    data() {
      return {
        searchTerm: '',
      };
    },
    methods: {
      ...mapMutations(['setSearchResults']),
      async search() {
        try {
          const response = await fetch(`http://localhost:8000/api/user/search`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              searched: this.searchTerm,
            }),
          });
  
          const data = await response.json();
          this.setSearchResults(data.searchResults);
          this.$router.push({ name: 'userSearch' });
        } catch (error) {
          console.error('Error fetching search results:', error);
        }
      },
    },
  };
  </script>
  