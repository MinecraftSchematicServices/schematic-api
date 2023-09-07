<?php

use Livewire\Volt\Component;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Cache;

new class extends Component {
    public $schematic;
    public $bitCount = 2;
    private $data = [
        'schematic_name' => 'test',
        'generator_type' => 'decoders',
        'generator_name' => 'five_hertz_y_decoder',
        'generator_args' => [
            'chiseled_bookshelves' => false,
            'bit_count' => 2,
        ],
    ];

    private function getSchematic($data)
    {
        $cacheKey = 'schematic-' . md5(json_encode($data));
        $cachedSchematic = Cache::remember($cacheKey, 60 * 60 * 24, function () use ($data) {
            $response = Http::post('host.docker.internal:8080/api/get-schematic', $data);
            //check the http status code
            if ($response->status() != 200) {
                dd($response->body());
                throw new \Exception('Failed to generate schematic');
            }
            $bytes = $response->body();
            return base64_encode($bytes);
        });
        $this->dispatch('schematicUpdated', schematic: $cachedSchematic);
        return $cachedSchematic;
    }

    public function mount()
    {
        $this->schematic = $this->getSchematic($this->data);
    }

    public function updatedBitCount()
    {
        $this->bitCount = intval($this->bitCount);
        $this->data['generator_args']['bit_count'] = $this->bitCount;
        $this->schematic = $this->getSchematic($this->data);
    }

}; ?>

<x-app-layout>
    <x-slot name="header">
        <h2 class="font-semibold text-xl text-gray-800 dark:text-gray-200 leading-tight">
            {{ __('Schematic') }}
        </h2>
    </x-slot>
    @volt
        <div>
            <p class="text-gray-500 dark:text-gray-400">Schematic</p>
            <input type="number" wire:model.live="bitCount"
                class="border border-gray-300 dark:border-gray-700 rounded-md shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50">
            <div class="mt-4 bg-white dark:bg-gray-800 overflow-hidden shadow sm:rounded-lg">
                <canvas id="schematicRenderer" width="500" height="500" class="!outline-none"></canvas>

            </div>
            <script type="module">

                let currentRender = null;

                function render(schematic) {
                    const canvas = document.querySelector('#schematicRenderer');
                    const schemFile = base64ToUint8Array(schematic.replace(/[^A-Za-z0-9+/=]/g, ""));

                    if (currentRender!=null) {
                        let babylonJsEngine = currentRender.getEngine();
                        currentRender.destroy();
                        const promise = babylonJsEngine.dispose();
                        currentRender = null;
                    }

                    let currentRenderPromise = renderSchematic(canvas, schemFile, {
                        size: 500,
                        renderArrow: false,
                        renderBars: false,
                        corsBypassUrl: '',
                        getClientJarUrl: async (props) => {
                            return await getCachedMinecraftJarUrl();
                        }
                    });
                    currentRenderPromise.then((render) => {
                        currentRender = render;
                    });
                }
                document.addEventListener('livewire:initialized', () => {
                    @this.on('schematicUpdated', (event) => {
                        render(event.schematic);
                    });
                 });
                 render(@json($schematic));
            </script>

        </div>
    @endvolt

</x-app-layout>
