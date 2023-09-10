<?php

use Livewire\Volt\Component;
use Livewire\WithFileUploads;
use Livewire\Attributes\Rule;

new class extends Component {
    use WithFileUploads;

    #[Rule('required')]
    public $schematicName = 'Schematic';

    #[Rule('required')]
    public $schematicFile;

    #[Rule('required')]
    public $previewImage;
    

    private function formatSchematicName($schematicName)
    {
        
        $schematicName = explode('.', $schematicName)[0];
        $schematicName = str_replace(' ', '_', $schematicName);
        $schematicName = preg_replace('/[^A-Za-z0-9\-]/', '', $schematicName);
        if (strlen($schematicName) > 20){
            $schematicName = str_split($schematicName, 20)[0];
        }
        if (strlen($schematicName) > 1){
            $schematicName = uniqid() . '-' . $schematicName;
        } else {
            $schematicName = uniqid();
        }
        $schematicName = $schematicName . '.schem';
        return $schematicName;
    }

    private function dataURLToFile($dataURL, $fileName)
    {
        $data = explode(',', $dataURL);
        $data = base64_decode($data[1]);
        $file = tempnam(sys_get_temp_dir(), 'livewire-tmp');
        file_put_contents($file, $data);
        return new \Illuminate\Http\UploadedFile($file, $fileName);
    }

    public function save()
    {


        dd($this->previewImage);
        $schematicName = $this->formatSchematicName($this->schematicName);

        $previewImage = $this->dataURLToFile($this->previewImage, $schematicName . '.png');
        $schematicUUID = uniqid();
        $schematicFile = $this->schematicFile;
        
        $disk = Storage::disk('minio');
        $disk->put('schematics/' . $schematicUUID . '.schem', $schematicFile);
        $disk->put('previews/' . $schematicUUID . '.png', $previewImage);
        return redirect('/schematic-browser');
    }


} ?>
<x-app-layout>
    <x-slot name="header">
        <h2 class="font-semibold text-xl text-white leading-tight">
            {{ __('Upload Schematic') }}
        </h2>
    </x-slot>
    @volt
        <div class="p-4 flex justify-center">
            <div class="items-center justify-center bg-base-100 rounded-lg shadow-md p-4 w-full md:w-1/3 xl:w-1/4">
                <form wire:submit="save">
                    <input type="hidden" id="previewImage" name="previewImage" wire:model="previewImage">

                    <div class="flex flex-col">
                        <div class="flex flex-col">
                            <label for="schematicName" class="text-sm font-bold text-white">Schematic
                                Name</label>
                            <input type="text" wire:model="schematicName" id="schematicName" name="schematicName"
                                class="w-full px-4 py-2 mt-2 text-white text-neutral bg-base-100 border border-primary rounded-lg focus:border-accent focus:outline-none focus:ring-2 focus:ring-accent"
                                placeholder="Schematic Name">

                            @error('schematicName')
                                <span class="text-error">{{ $message }}</span>
                            @enderror
                        </div>
                        <div class="flex flex-col mt-4">
                            <div id="spinner" class="flex justify-center items-center p-4 hidden" wire:ignore>
                                <span class="loading loading-lg loading-primary"></span>
                            </div>
                            <div id="preview" class="relative mt-4 hidden" x-cloak>
                                <canvas wire:ignore id="preview_canvas"class="!outline-none" width="1000"
                                    height="1000"></canvas>
                                <button id="delete-button" type="button"
                                    class="absolute bottom-0 right-0 px-4 py-2 text-error">
                                    <i class="fas fa-trash"></i>
                                </button>
                            </div>

                            <div x-data="{ uploading: false, progress: 0 }" x-on:livewire-upload-start="uploading = true"
                                x-on:livewire-upload-finish="uploading = false"
                                x-on:livewire-upload-error="uploading = false"
                                x-on:livewire-upload-progress="progress = $event.detail.progress">
                                <div id="dropzone" wire:ignore
                                    class="p-10 border-2 border-dashed border-gray-300 rounded-lg text-center cursor-pointer text-white"
                                    x-data="{ isDragging: false }"
                                    @dragover.prevent="$event.dataTransfer.dropEffect = 'copy'; isDragging = true"
                                    @dragleave="isDragging = false"
                                    @drop.prevent="isDragging = false; $refs.schematicFile.files = $event.dataTransfer.files; handleFileChange()"
                                    @click="$refs.schematicFile.click()">
                                    <span id="dropzone-text" class="block"
                                        x-text="isDragging ? 'Drop it!' : 'Drag & Drop a Schematic File or select one'"></span>
                                    <span id="loading-spinner" class="loading loading-spinner loading-md hidden"></span>
                                    <input type="file" id="schematicFile" name="schematicFile" class="hidden"
                                        wire:model="schematicFile" x-ref="schematicFile" @change="handleFileChange">
                                    <button type="button" id="cancel-button"
                                        class="hidden mt-5 px-4 py-2 text-white font-semibold text-neutral bg-error rounded-lg shadow-md hover:bg-opacity-80">Cancel</button>

                                    @error('schematicFile')
                                        <span class="text-error">{{ $message }}</span>
                                    @enderror

                                    <div x-cloak x-show="uploading || progress > 0" class="relative pt-1">
                                        <div class="flex mb-2 items-center justify-between">
                                            <div>
                                                <span class="text-xs font-semibold inline-block  text-white"
                                                    x-text="(progress == 100) ? 'Uploaded !' : progress + '%'"
                                                    :class="{ 'text-success': progress == 100 }">
                                                    0%
                                                </span>
                                                <i class="fas fa-check text-success" x-show="progress == 100"></i>

                                            </div>
                                            <div class="text-right">
                                                <span class="text-xs font-semibold inline-block  text-white"
                                                    x-text="progress + '%'">
                                                    0%
                                                </span>
                                            </div>
                                        </div>
                                        <div class="overflow-hidden h-2 mb-4 text-xs flex rounded bg-base-100">
                                            <div style="width:0%"
                                                class="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-primary"
                                                x-bind:style="'width:' + progress + '%'"></div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="flex flex-col mt-4">
                            <button type="submit"
                                class="px-4 py-2 text-white font-semibold text-neutral transition duration-200 ease-in bg-primary rounded-lg shadow-md hover:bg-opacity-80 focus:ring-accent focus:ring-offset-accent focus:outline-none focus:ring-2 focus:ring-offset-2">Submit</button>
                        </div>
                    </div>
                </form>
            </div>
        </div>



        <script>
            let schematicFileUploadInput = document.getElementById('schematicFile');
            let currentRender = null;
            const previewCanvas = document.getElementById('preview_canvas');
            const canvasParent = previewCanvas.parentElement;
            const canvasParentParent = canvasParent.parentElement;
            if (canvasParentParent.clientWidth < previewCanvas.width) {
                previewCanvas.style.width = canvasParentParent.clientWidth + 'px';
                previewCanvas.style.height = canvasParentParent.clientWidth + 'px';
            }
            let size = 1000;

            function setCanvasState(state) {
                const preview = document.getElementById('preview');
                if (state) {
                    preview.classList.remove('hidden');
                } else {
                    preview.classList.add('hidden');

                }
            }

            function setDropzoneState(state) {
                const dropzone = document.getElementById('dropzone');
                
                if (state) {
                    console.log('Showing dropzone');
                    dropzone.classList.remove('hidden');
                } else {
                    console.log('Hiding dropzone');
                    dropzone.classList.add('hidden');
                }
            }

            function setSpinnerState(state) {
                const spinner = document.getElementById('spinner');
                if (state) {
                    console.log('Showing spinner');
                    spinner.classList.remove('hidden');
                } else {
                    console.log('Hiding spinner');
                    spinner.classList.add('hidden');
                }
            }

            function renderSchematicPreview(schematicFile) {
                setCanvasState(false);
                setDropzoneState(false);
                setSpinnerState(true);
                const canvasParent = previewCanvas.parentElement;
                const canvasParentParent = canvasParent.parentElement;
                if (canvasParentParent.clientWidth < previewCanvas.width) {
                    previewCanvas.style.width = canvasParentParent.clientWidth + 'px';
                    previewCanvas.style.height = canvasParentParent.clientWidth + 'px';
                }
                if (currentRender != null) {
                    let babylonJsEngine = currentRender.getEngine();
                    currentRender.destroy();
                    const promise = babylonJsEngine.dispose();
                    currentRender = null;
                }
                let currentRenderPromise = renderSchematic(previewCanvas, schematicFile, {
                    renderArrow: false,
                    renderBars: false,
                    corsBypassUrl: '',
                    orbitSpeed: 0,
                    getClientJarUrl: async (props) => {
                        return await getCachedMinecraftJarUrl();
                    }
                });
                currentRenderPromise.then((render) => {
                    currentRender = render;
                    setSpinnerState(false);
                    setCanvasState(true);
                    const babyloneJsEngine = render.getEngine();
                    const camera = babyloneJsEngine.scenes[0].cameras[0];
                    const image = BABYLON.Tools.CreateScreenshot(babyloneJsEngine, camera, {
                    width: size,
                        height: size
                    },function(data) {
                        console.log(data);
                        const previewImage = document.getElementById('previewImage');
                        previewImage.value = data;
                        
                    }); 
                    //setTimeout(() => {
                    //    
                    //}, 100);
                });
            }
            schematicFileUploadInput.addEventListener('change', function(event) {
                schematicFilePromise = event.target.files[0].arrayBuffer().then((buffer) => {
                    return new Uint8Array(buffer);
                });
                schematicFilePromise.then((file) => {
                    renderSchematicPreview(file);

                });
            });

            function handleFileChange() {
                const fileInput = document.getElementById('schematicFile');
                const file = fileInput.files[0];
                if (file) {
                    schematicFilePromise = file.arrayBuffer().then((buffer) => {
                        return new Uint8Array(buffer);
                    });
                    schematicFilePromise.then((file) => {
                        renderSchematicPreview(file);

                    });
                }
            }



            document.getElementById('cancel-button').addEventListener('click', function() {
                const fileInput = document.getElementById('schematicFile');
                fileInput.value = null;
                //clear the progress bar
                const progressBar = document.querySelector('#dropzone .h-2');
                progressBar.style.width = '0%';
                progressBar.parentElement.parentElement.classList.add('hidden');
                setCanvasState(false);
                
            });

            document.getElementById('delete-button').addEventListener('click', function() {
                console.log('delete');
                const fileInput = document.getElementById('schematicFile');
                fileInput.value = null;
                setCanvasState(false);
                setDropzoneState(true);
            });
        </script>
    @endvolt
</x-app-layout>
