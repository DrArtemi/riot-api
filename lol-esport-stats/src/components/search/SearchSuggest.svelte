<script>
    import SearchCategory from "./SearchCategory.svelte";

    export let search_data;
</script>


{#each search_data as { category, data }, i}
    {#if data.length > 0}
        <div class="search-category">
            <SearchCategory name={category} data={data}/>
        </div>
    {/if}
{/each}

<style>
</style>