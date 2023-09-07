import './bootstrap';
import * as utils from './utils';
import bufferModule from 'buffer';
import * as schematicwebviewer from '@enginehub/schematicwebviewer';

Object.assign(window, utils);
window.Buffer = bufferModule.Buffer;
window.renderSchematic = schematicwebviewer.renderSchematic;
