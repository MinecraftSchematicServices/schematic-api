<?php

use Livewire\Volt\Component;
use Illuminate\Support\Facades\Http;

new class extends Component {
    public $schematic;
    public function mount()
    {
        $response = Http::post('host.docker.internal:8080/api/get-schematic', [
            'schematic_name' => 'test',
            'generator_type' => 'decoders',
            'generator_name' => 'five_hertz_y_decoder',
            'generator_args' => [
                'chiseled_bookshelves' => false,
                'bit_count' => 4,
            ]
        ]);
        $bytes = $response->body();
        $this->schematic = base64_encode($bytes);
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
            <p class="text-gray-500 dark:text-gray-400">This is the schematic page.sadfasdf</p>
            <canvas id="schematicRenderer" width="500" height="500"></canvas>
            <script type="module">
                function base64ToUint8Array(base64) {
                    const binaryString = atob(base64);
                    const len = binaryString.length;
                    const bytes = new Uint8Array(len);
                    for (let i = 0; i < len; i++) {
                        bytes[i] = binaryString.charCodeAt(i);
                    }
                    return bytes;
                }

                const schemBase64 = '@json($schematic)';
                const cleanedSchemBase64 = schemBase64.replace(/[^A-Za-z0-9+/=]/g, "");
                const schemFile = base64ToUint8Array(cleanedSchemBase64);
                window.schemFile = schemFile;
                renderSchematic(document.querySelector('#schematicRenderer'), schemFile, {
                    size: 500,
                    renderArrow: false,
                    renderBars: false,
                    corsBypassUrl: 'https://cors-anywhere.herokuapp.com/',
                });

            </script>
        </div>
    @endvolt

</x-app-layout>
