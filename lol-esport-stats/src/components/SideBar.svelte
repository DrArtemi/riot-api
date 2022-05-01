<script>
    export let title;
    export let tabs;
    export let activeTab;

    function activate(e) {
        activeTab = parseInt(e.target.dataset.id);
    }
</script>

<div class="w-full h-full">
    <h1 class="text-4xl px-4 py-8 capitalize text-slate-400">{title}</h1>
    <ul>
        {#each tabs as tab, i}
        <li
            data-id="{i}"
            on:click={activate}
            class="text-slate-200 px-4 py-4 border-t border-slate-900 hover:bg-slate-700 hover:cursor-pointer capitalize {i === activeTab ? 'active bg-slate-700' : ''}"
        >{tab}</li>
        {/each}
    </ul>
</div>
