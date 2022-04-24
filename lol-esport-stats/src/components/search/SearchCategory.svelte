<script>
    import SearchItem from "./SearchItem.svelte";

    export let name;
    export let data;
</script>

<span class="category-name">{name}</span>
<ul class="search-category">
    {#each data as el (el.id)}
        <SearchItem name={el.name} link="/{name.toLowerCase()}?slug={el.slug}"/>
    {/each}
</ul>

<style>
    .category-name {
        color: #455a64;
    }

    .search-category {
        padding-left: 0;
    }
</style>