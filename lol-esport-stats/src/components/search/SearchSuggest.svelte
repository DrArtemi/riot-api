<script>
    import SearchCategory from "./SearchCategory.svelte";

    export let search_data;
</script>


<div class="border-t-2 border-t-slate-600">
{#each search_data as { category, data }, i}
    {#if data.length > 0}
        <SearchCategory name={category} data={data}/>
    {/if}
{/each}
</div>
