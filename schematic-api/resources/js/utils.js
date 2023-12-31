import pako from 'pako';

export async function openDatabase() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open("minecraftDB", 1);

        request.onupgradeneeded = function(event) {
            const db = event.target.result;
            if (!db.objectStoreNames.contains('jars')) {
                db.createObjectStore('jars');
            }
        };

        request.onsuccess = function(event) {
            resolve(event.target.result);
        };

        request.onerror = function(event) {
            reject("Error opening IndexedDB.");
        };
    });
}

export async function getCachedMinecraftJarUrl() {
    console.log("Getting cached Minecraft jar URL...");
    const jarURL = 'https://launcher.mojang.com/v1/objects/c0898ec7c6a5a2eaa317770203a1554260699994/client.jar';
    const jarUrlHash = 'c0898ec7c6a5a2eaa317770203a1554260699994';
    const db = await openDatabase();
    const transaction = db.transaction(["jars"], "readonly");
    const objectStore = transaction.objectStore("jars");
    const request = objectStore.get(jarUrlHash);

    return new Promise(async (resolve, reject) => {
        request.onsuccess = function(event) {
            if (request.result) {
                console.log("Jar found in IndexedDB.");
                resolve(URL.createObjectURL(request.result));
            } else {
                console.log("Jar not found in IndexedDB, fetching from Mojang...");
                const corsBypassUrl = 'https://cors-anywhere.herokuapp.com/';
                fetch(corsBypassUrl + jarURL).then(response => response.blob()).then(blob => {
                    const addRequest = db.transaction(["jars"], "readwrite").objectStore("jars").add(blob, jarUrlHash);
                    addRequest.onsuccess = function(event) {
                        resolve(URL.createObjectURL(blob));
                    };
                    addRequest.onerror = function(event) {
                        reject("Error storing jar in IndexedDB.");
                    };
                });
            }
        };

        request.onerror = function(event) {
            reject("Error fetching jar from IndexedDB.");
        };
    });
}

export function dataURLToBlob(dataURL) {
    let binary = atob(dataURL.split(',')[1]);
    let array = [];
    for (let i = 0; i < binary.length; i++) {
        array.push(binary.charCodeAt(i));
    }
    return new Blob([new Uint8Array(array)], {type: 'image/png'});
}

export function base64ToUint8Array(base64) {
    const binaryString = atob(base64);
    const len = binaryString.length;
    const bytes = new Uint8Array(len);
    for (let i = 0; i < len; i++) {
        bytes[i] = binaryString.charCodeAt(i);
    }
    return bytes;
}


export function base64ToGzip(base64) {
    console.log(base64);
    return pako.inflate(base64ToUint8Array(base64), { to: 'string' });
}
