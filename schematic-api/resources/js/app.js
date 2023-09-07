import './bootstrap';
import bufferModule from 'buffer';
import * as schematicwebviewer from '@enginehub/schematicwebviewer';

window.Buffer = bufferModule.Buffer;
window.renderSchematic = schematicwebviewer.renderSchematic;
