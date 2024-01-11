(self["webpackChunkipywebgl"] = self["webpackChunkipywebgl"] || []).push([["lib_widgets_js"],{

/***/ "./lib/arraybuffer.js":
/*!****************************!*\
  !*** ./lib/arraybuffer.js ***!
  \****************************/
/***/ ((__unused_webpack_module, exports) => {

"use strict";

Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.buffer_to_array = void 0;
function buffer_to_array(dtype, buffer) {
    switch (dtype) {
        case 'int8':
            return new Int8Array(buffer);
            break;
        case 'uint8':
            return new Uint8Array(buffer);
            break;
        case 'int16':
            return new Int16Array(buffer);
            break;
        case 'uint16':
            return new Uint16Array(buffer);
            break;
        case 'int32':
            return new Int32Array(buffer);
            break;
        case 'uint32':
            return new Uint32Array(buffer);
            break;
        case 'float32':
            return new Float32Array(buffer);
            break;
        case 'float64':
            return new Float64Array(buffer);
            break;
        default:
            throw 'Unknown dtype ' + dtype;
            break;
    }
}
exports.buffer_to_array = buffer_to_array;
//# sourceMappingURL=arraybuffer.js.map

/***/ }),

/***/ "./lib/glresource.js":
/*!***************************!*\
  !*** ./lib/glresource.js ***!
  \***************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";

Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.GLResourceView = exports.GLResource = void 0;
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
const version_1 = __webpack_require__(/*! ./version */ "./lib/version.js");
// Import the CSS
__webpack_require__(/*! ../css/widget.css */ "./css/widget.css");
class GLResource extends base_1.DOMWidgetModel {
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: 'GLResource', _model_module: version_1.MODULE_NAME, _model_module_version: version_1.MODULE_VERSION, _view_name: 'GLResourceView', _view_module: version_1.MODULE_NAME, _view_module_version: version_1.MODULE_VERSION, _context: null, _gl_ptr: null, _info: { type: 'not set' }, uid: 0 });
    }
    initialize(attributes, options) {
        super.initialize(attributes, options);
        this.get('_context').register_resource(this);
    }
}
exports.GLResource = GLResource;
GLResource.serializers = Object.assign(Object.assign({}, base_1.DOMWidgetModel.serializers), { _context: { deserialize: base_1.unpack_models } });
class GLResourceView extends base_1.DOMWidgetView {
    render() {
        const root = this.el;
        const jsonDisplay = document.createElement("div");
        jsonDisplay.classList.add("ipywebgl-json-display");
        const jsonKey = document.createElement("div");
        jsonKey.classList.add("ipywebgl-json-key");
        jsonKey.textContent = "uid:";
        const jsonValue = document.createElement("div");
        jsonValue.classList.add("ipywebgl-json-value");
        jsonValue.textContent = this.model.get('uid');
        jsonDisplay.appendChild(jsonKey);
        jsonDisplay.appendChild(jsonValue);
        this.displayJson(this.model.get('_info'), jsonDisplay);
        root.appendChild(jsonDisplay);
    }
    displayJson(json, parent) {
        for (const key in json) {
            const jsonKey = document.createElement("div");
            jsonKey.classList.add("ipywebgl-json-key");
            jsonKey.textContent = `${key}:`;
            const jsonValue = document.createElement("div");
            jsonValue.classList.add("ipywebgl-json-value");
            if (typeof json[key] === "object") {
                const nestedJsonDisplay = document.createElement("div");
                nestedJsonDisplay.classList.add("ipywebgl-json-display");
                this.displayJson(json[key], nestedJsonDisplay);
                jsonValue.appendChild(nestedJsonDisplay);
            }
            else {
                jsonValue.textContent = json[key];
            }
            parent.appendChild(jsonKey);
            parent.appendChild(jsonValue);
        }
    }
}
exports.GLResourceView = GLResourceView;
//# sourceMappingURL=glresource.js.map

/***/ }),

/***/ "./lib/glviewer.js":
/*!*************************!*\
  !*** ./lib/glviewer.js ***!
  \*************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";

Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.GLViewer = exports.GLModel = void 0;
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
const version_1 = __webpack_require__(/*! ./version */ "./lib/version.js");
const matrix_1 = __webpack_require__(/*! ./matrix */ "./lib/matrix.js");
const arraybuffer_1 = __webpack_require__(/*! ./arraybuffer */ "./lib/arraybuffer.js");
function serializeImageData(array) {
    console.log('serialized');
    console.log(array);
    return new DataView(array.buffer.slice(0));
}
function deserializeImageData(dataview) {
    if (dataview === null) {
        return null;
    }
    return new Uint8ClampedArray(dataview.buffer);
}
class GLModel extends base_1.DOMWidgetModel {
    constructor() {
        super(...arguments);
        this.resources = [];
        this.bound_buffers = {};
        this.commands = [];
        this.buffers = [];
    }
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: 'GLModel', _model_module: version_1.MODULE_NAME, _model_module_version: version_1.MODULE_VERSION, _view_name: 'GLViewer', _view_module: version_1.MODULE_NAME, _view_module_version: version_1.MODULE_VERSION, shader_matrix_major: 'row_major', width: 700, height: 500, camera_pos: [0, 50, 200], camera_yaw: 0, camera_pitch: 0, camera_fov: 50.0, camera_near: 1.0, camera_far: 5000.0, mouse_speed: 1, move_speed: 1, move_keys: 'wasd', sync_image_data: false, image_data: null, verbose: 0 });
    }
    initialize(attributes, options) {
        super.initialize(attributes, options);
        this.canvas = document.createElement('canvas');
        this.ctx = this.canvas.getContext("webgl2", { preserveDrawingBuffer: true });
        if (this.ctx == null) {
            console.error('could not create a webgl2 context, this is not supported in your browser');
        }
        else {
            const gl = this.ctx;
            this.view_block = gl.createBuffer();
            gl.bindBuffer(gl.UNIFORM_BUFFER, this.view_block);
            gl.bufferData(gl.UNIFORM_BUFFER, 256, gl.DYNAMIC_DRAW);
            gl.bindBuffer(gl.UNIFORM_BUFFER, null);
            gl.bindBufferBase(gl.UNIFORM_BUFFER, 0, this.view_block);
            //extensions to activate
            gl.getExtension("EXT_color_buffer_float");
        }
        this.resizeCanvas();
        this.on_some_change(['width', 'height', 'camera_fov', 'camera_near', 'camera_far'], this.resizeCanvas, this);
        this.on_some_change(['camera_pos', 'camera_yaw', 'camera_pitch'], this.run_commands, this);
        this.on('msg:custom', this.handle_custom_messages, this);
        this.camera_matrix = matrix_1.m4Translation(0, 50, 200);
        this.view_matrix = matrix_1.m4inverse(this.camera_matrix);
    }
    resizeCanvas() {
        this.canvas.setAttribute('width', this.get('width'));
        this.canvas.setAttribute('height', this.get('height'));
        if (this.ctx != null) {
            this.ctx.viewport(0, 0, this.ctx.canvas.width, this.ctx.canvas.height);
        }
        this.projection_matrix = matrix_1.m4ProjectionMatrix(this.get('camera_fov'), this.get('width') / this.get('height'), this.get('camera_near'), this.get('camera_far'));
    }
    handle_custom_messages(command, buffers) {
        if (command.clear == true) {
            this.commands = [];
            this.buffers = [];
        }
        let commands = command.commands;
        let converted_buffers = [];
        commands.forEach((element) => {
            if (element.hasOwnProperty('buffer_metadata')) {
                const converted = arraybuffer_1.buffer_to_array(element.buffer_metadata.dtype, buffers[element.buffer_metadata.index].buffer);
                converted_buffers.push(converted);
            }
        });
        if (command.only_once == true) {
            this.execute_commands(commands, converted_buffers);
        }
        else {
            let buffer_id_offset = this.buffers.length;
            this.buffers = this.buffers.concat(converted_buffers);
            commands.forEach((element) => {
                if (element.hasOwnProperty('buffer_metadata')) {
                    element.buffer_metadata.index += buffer_id_offset;
                }
            });
            this.commands = this.commands.concat(commands);
        }
        this.run_commands();
    }
    update_camera() {
        let pos = this.get('camera_pos');
        let yaw = this.get('camera_yaw') * Math.PI / 180.0;
        let pitch = this.get('camera_pitch') * Math.PI / 180.0;
        this.camera_matrix = matrix_1.m4Translation(pos[0], pos[1], pos[2]);
        this.camera_matrix = matrix_1.m4dot(this.camera_matrix, matrix_1.m4Yrotation(yaw));
        this.camera_matrix = matrix_1.m4dot(this.camera_matrix, matrix_1.m4Xrotation(pitch));
        this.view_matrix = matrix_1.m4inverse(this.camera_matrix);
        this.view_proj_matrix = matrix_1.m4dot(this.projection_matrix, this.view_matrix);
    }
    run_commands() {
        this.execute_commands(this.commands, this.buffers);
    }
    execute_commands(commands, converted_buffers) {
        if (this.ctx == null)
            return;
        const gl = this.ctx;
        this.update_camera();
        // update the uniform Block
        let cm = (this.get('shader_matrix_major') == 'row_major') ? matrix_1.m4Transpose(this.camera_matrix) : this.camera_matrix;
        const cm_f32 = new Float32Array(cm);
        let vm = (this.get('shader_matrix_major') == 'row_major') ? matrix_1.m4Transpose(this.view_matrix) : this.view_matrix;
        const vm_f32 = new Float32Array(vm);
        let pm = (this.get('shader_matrix_major') == 'row_major') ? matrix_1.m4Transpose(this.projection_matrix) : this.projection_matrix;
        const pm_f32 = new Float32Array(pm);
        let vpm = (this.get('shader_matrix_major') == 'row_major') ? matrix_1.m4Transpose(this.view_proj_matrix) : this.view_proj_matrix;
        const vpm_f32 = new Float32Array(vpm);
        gl.bindBuffer(gl.UNIFORM_BUFFER, this.view_block);
        gl.bufferSubData(gl.UNIFORM_BUFFER, 0, cm_f32, 0);
        gl.bufferSubData(gl.UNIFORM_BUFFER, 64, vm_f32, 0);
        gl.bufferSubData(gl.UNIFORM_BUFFER, 128, pm_f32, 0);
        gl.bufferSubData(gl.UNIFORM_BUFFER, 192, vpm_f32, 0);
        gl.bindBuffer(gl.UNIFORM_BUFFER, null);
        commands.forEach((command) => {
            this.execute_command(gl, command, converted_buffers);
        });
        if (this.get('sync_image_data')) {
            const width = this.get('width');
            const height = this.get('height');
            const pixels = new Uint8ClampedArray(width * height * 4);
            gl.readPixels(0, 0, width, height, gl.RGBA, gl.UNSIGNED_BYTE, pixels);
            this.set('image_data', pixels);
            this.save_changes();
            console.log('rendered');
            console.log(pixels);
        }
    }
    glEnumToString(gl, value) {
        const keys = [];
        for (const key in gl) {
            if (gl[key] === value) {
                keys.push(key);
            }
        }
        return keys.length ? keys.join(' | ') : `0x${value.toString(16)}`;
    }
    execute_command(gl, command, converted_buffers) {
        if (this.get('verbose') > 0) {
            console.log(command);
            if (command.hasOwnProperty('buffer_metadata')) {
                console.log('data');
                console.log(converted_buffers[command.buffer_metadata.index]);
            }
        }
        //console.log(this.bound_buffers);
        switch (command.cmd) {
            case 'viewport':
                gl.viewport(command.x, command.y, command.width, command.height);
                break;
            case 'enable':
            case 'disable':
                {
                    let cap = 0;
                    if (command.blend)
                        cap |= gl.BLEND;
                    if (command.depth_test)
                        cap |= gl.DEPTH_TEST;
                    if (command.dither)
                        cap |= gl.DITHER;
                    if (command.polygon_offset_fill)
                        cap |= gl.POLYGON_OFFSET_FILL;
                    if (command.sample_alpha_to_coverage)
                        cap |= gl.SAMPLE_ALPHA_TO_COVERAGE;
                    if (command.sample_coverage)
                        cap |= gl.SAMPLE_COVERAGE;
                    if (command.scissor_test)
                        cap |= gl.SCISSOR_TEST;
                    if (command.stencil_test)
                        cap |= gl.STENCIL_TEST;
                    if (command.rasterizer_discard)
                        cap |= gl.RASTERIZER_DISCARD;
                    if (command.cull_face)
                        cap |= gl.CULL_FACE;
                    if (command.cmd == 'enable') {
                        gl.enable(cap);
                    }
                    else {
                        gl.disable(cap);
                    }
                }
                break;
            case 'clearColor':
                gl.clearColor(command.r, command.g, command.b, command.a);
                break;
            case 'clear':
                {
                    let bits = 0;
                    if (command.depth)
                        bits |= gl.DEPTH_BUFFER_BIT;
                    if (command.color)
                        bits |= gl.COLOR_BUFFER_BIT;
                    if (command.stencil)
                        bits |= gl.STENCIL_BUFFER_BIT;
                    gl.clear(bits);
                }
                break;
            case 'frontFace':
                {
                    gl.frontFace(gl[command.mode]);
                }
                break;
            case 'cullFace':
                {
                    gl.cullFace(gl[command.mode]);
                }
                break;
            // ------------------------------- DEPTH --------------------------------------
            case 'depthFunc':
                {
                    gl.depthFunc(gl[command.func]);
                }
                break;
            case 'depthMask':
                {
                    gl.depthMask(command.flag);
                }
                break;
            case 'depthRange':
                {
                    gl.depthRange(command.z_near, command.z_far);
                }
                break;
            // ------------------------------- COLOR --------------------------------------
            case 'blendColor':
                gl.blendColor(command.r, command.g, command.b, command.a);
                break;
            case 'blendEquation':
                gl.blendEquation(gl[command.mode]);
                break;
            case 'blendEquationSeparate':
                gl.blendEquationSeparate(gl[command.mode_rgb], gl[command.mode_alpha]);
                break;
            case 'blendFunc':
                gl.blendFunc(gl[command.s_factor], gl[command.d_factor]);
                break;
            case 'blend_func_separate':
                gl.blendFuncSeparate(gl[command.src_rgb], gl[command.dst_rgb], gl[command.src_alpha], gl[command.dst_alpha]);
                break;
            // ------------------------------- TEXTURE --------------------------------------
            case 'createTexture':
                {
                    let res = this.get_resource(command.resource);
                    const ptr = gl.createTexture();
                    res.set('_gl_ptr', ptr);
                    res.set('_info', { type: 'texture' });
                    res.save_changes();
                }
                break;
            case 'bindTexture':
                {
                    if (command.texture > -1) {
                        const texture = this.get_resource(command.texture).get('_gl_ptr');
                        gl.bindTexture(gl[command.target], texture);
                    }
                    else {
                        gl.bindTexture(gl[command.target], null);
                    }
                }
                break;
            case 'activeTexture':
                gl.activeTexture(gl.TEXTURE0 + command.texture);
                break;
            case 'generateMipmap':
                gl.generateMipmap(gl[command.target]);
                break;
            case 'texImage2D':
                if (command.hasOwnProperty('buffer_metadata')) {
                    gl.texImage2D(gl[command.target], command.level, gl[command.internal_format], command.width, command.height, command.border, gl[command.format], gl[command.data_type], converted_buffers[command.buffer_metadata.index]);
                }
                else {
                    gl.texImage2D(gl[command.target], command.level, gl[command.internal_format], command.width, command.height, command.border, gl[command.format], gl[command.data_type], null);
                }
                break;
            case 'texStorage2D':
                {
                    gl.texStorage2D(gl[command.target], command.levels, gl[command.internal_format], command.width, command.height);
                }
                break;
            case 'texImage3D':
                if (command.hasOwnProperty('buffer_metadata')) {
                    gl.texImage3D(gl[command.target], command.level, gl[command.internal_format], command.width, command.height, command.depth, command.border, gl[command.format], gl[command.data_type], converted_buffers[command.buffer_metadata.index]);
                }
                else {
                    gl.texImage3D(gl[command.target], command.level, gl[command.internal_format], command.width, command.height, command.depth, command.border, gl[command.format], gl[command.data_type], null);
                }
                break;
            case 'texStorage3D':
                {
                    gl.texStorage3D(gl[command.target], command.levels, gl[command.internal_format], command.width, command.height, command.depth);
                }
                break;
            case 'texParameteri':
                gl.texParameteri(gl[command.target], gl[command.pname], command.param);
                break;
            case 'texParameterf':
                gl.texParameterf(gl[command.target], gl[command.pname], command.param);
                break;
            case 'texParameter_str':
                gl.texParameteri(gl[command.target], gl[command.pname], gl[command.param]);
                break;
            case 'pixelStorei':
                {
                    if (command.pname == 'UNPACK_COLORSPACE_CONVERSION_WEBGL') {
                        gl.pixelStorei(gl[command.pname], gl[command.param]);
                    }
                    else {
                        gl.pixelStorei(gl[command.pname], command.param);
                    }
                }
                break;
            // ------------------------------- SHADERS --------------------------------------
            case 'createShader':
                {
                    let res = this.get_resource(command.resource);
                    const ptr = gl.createShader(gl[command.type]);
                    res.set('_gl_ptr', ptr);
                    res.set('_info', { type: command.type });
                    res.save_changes();
                }
                break;
            case 'shaderSource':
                {
                    const res = this.get_resource(command.shader);
                    const ptr = res.get('_gl_ptr');
                    gl.shaderSource(ptr, command.source);
                }
                break;
            case 'compileShader':
                {
                    const res = this.get_resource(command.shader);
                    const ptr = res.get('_gl_ptr');
                    gl.compileShader(ptr);
                    let resinfo = res.get('_info');
                    if (!gl.getShaderParameter(ptr, gl.COMPILE_STATUS)) {
                        let info = gl.getShaderInfoLog(ptr);
                        resinfo.message = info;
                    }
                    else {
                        resinfo.message = 'compiled';
                    }
                    res.set('_info', resinfo);
                    res.save_changes();
                }
                break;
            // ------------------------------- PROGRAMS --------------------------------------
            case 'createProgram':
                {
                    let res = this.get_resource(command.resource);
                    const ptr = gl.createProgram();
                    res.set('_gl_ptr', ptr);
                    res.set('_info', { type: 'Program' });
                    res.save_changes();
                }
                break;
            case 'attachShader':
                {
                    const prog = this.get_resource(command.program).get('_gl_ptr');
                    const shader = this.get_resource(command.shader).get('_gl_ptr');
                    gl.attachShader(prog, shader);
                }
                break;
            case 'bindAttribLocation':
                {
                    let res = this.get_resource(command.program);
                    const ptr = res.get('_gl_ptr');
                    gl.bindAttribLocation(ptr, command.index, command.name);
                }
                break;
            case 'linkProgram':
                {
                    let res = this.get_resource(command.program);
                    const ptr = res.get('_gl_ptr');
                    gl.linkProgram(ptr);
                    gl.validateProgram(ptr);
                    let resinfo = res.get('_info');
                    if (!gl.getProgramParameter(ptr, gl.LINK_STATUS)) {
                        let info = gl.getShaderInfoLog(ptr);
                        resinfo.message = info;
                    }
                    else {
                        //bind our viewBlock
                        let viewBlockIndex = gl.getUniformBlockIndex(ptr, 'ViewBlock');
                        if (viewBlockIndex < 4294967295) {
                            gl.uniformBlockBinding(ptr, viewBlockIndex, 0);
                        }
                        resinfo.message = 'linked';
                        resinfo.uniforms_blocks = [];
                        resinfo.uniforms = [];
                        const numUniforms = gl.getProgramParameter(ptr, gl.ACTIVE_UNIFORMS);
                        const indices = [...Array(numUniforms).keys()];
                        const blockIndices = gl.getActiveUniforms(ptr, indices, gl.UNIFORM_BLOCK_INDEX);
                        const offsets = gl.getActiveUniforms(ptr, indices, gl.UNIFORM_OFFSET);
                        for (let i = 0; i < numUniforms; ++i) {
                            const info = gl.getActiveUniform(ptr, i);
                            if (info) {
                                // regroup the blocks
                                if (blockIndices[i] > -1) {
                                    let uniform_block = resinfo.uniforms_blocks.find((element) => { return element.index == blockIndices[i]; });
                                    if (uniform_block == undefined) {
                                        uniform_block = {
                                            index: blockIndices[i],
                                            name: gl.getActiveUniformBlockName(ptr, blockIndices[i]),
                                            size: gl.getActiveUniformBlockParameter(ptr, blockIndices[i], gl.UNIFORM_BLOCK_DATA_SIZE),
                                            uniforms: []
                                        };
                                        resinfo.uniforms_blocks.push(uniform_block);
                                    }
                                    uniform_block.uniforms.push({ name: info.name, type: this.glEnumToString(gl, info.type), size: info.size, offset: offsets[i] });
                                }
                                else {
                                    resinfo.uniforms.push({ name: info.name, type: this.glEnumToString(gl, info.type), size: info.size, location: gl.getUniformLocation(ptr, info.name) });
                                }
                            }
                        }
                        resinfo.attributes = [];
                        const numAttribute = gl.getProgramParameter(ptr, gl.ACTIVE_ATTRIBUTES);
                        for (let i = 0; i < numAttribute; ++i) {
                            const info = gl.getActiveAttrib(ptr, i);
                            if (info)
                                resinfo.attributes.push({ name: info.name, type: this.glEnumToString(gl, info.type), size: info.size, location: gl.getAttribLocation(ptr, info.name) });
                        }
                    }
                    res.set('_info', resinfo);
                    res.save_changes();
                }
                break;
            case 'useProgram':
                {
                    if (command.program >= 0) {
                        const res = this.get_resource(command.program);
                        const ptr = res.get('_gl_ptr');
                        gl.useProgram(ptr);
                        this.bound_program = res;
                    }
                    else {
                        gl.useProgram(null);
                        this.bound_program = null;
                    }
                }
                break;
            case 'uniform':
            case 'uniformMatrix':
                {
                    if (this.bound_program != null) {
                        let resinfo = this.bound_program.get('_info');
                        const uniform = resinfo.uniforms.find((element) => { return element.name == command.name; });
                        if (uniform != undefined) {
                            const location = uniform.location;
                            if (command.cmd == 'uniform') {
                                let shape = command.buffer_metadata.shape[command.buffer_metadata.shape.length - 1];
                                if (command.buffer_metadata.dtype == 'int32') {
                                    let bufarray = converted_buffers[command.buffer_metadata.index];
                                    if (shape == 1)
                                        gl.uniform1iv(location, bufarray);
                                    else if (shape == 2)
                                        gl.uniform2iv(location, bufarray);
                                    else if (shape == 3)
                                        gl.uniform3iv(location, bufarray);
                                    else if (shape == 4)
                                        gl.uniform4iv(location, bufarray);
                                }
                                else if (command.buffer_metadata.dtype == 'uint32') {
                                    let bufarray = converted_buffers[command.buffer_metadata.index];
                                    if (shape == 1)
                                        gl.uniform1uiv(location, bufarray);
                                    else if (shape == 2)
                                        gl.uniform2uiv(location, bufarray);
                                    else if (shape == 3)
                                        gl.uniform3uiv(location, bufarray);
                                    else if (shape == 4)
                                        gl.uniform4uiv(location, bufarray);
                                }
                                else if (command.buffer_metadata.dtype == 'float32') {
                                    let bufarray = converted_buffers[command.buffer_metadata.index];
                                    if (shape == 1)
                                        gl.uniform1fv(location, bufarray);
                                    else if (shape == 2)
                                        gl.uniform2fv(location, bufarray);
                                    else if (shape == 3)
                                        gl.uniform3fv(location, bufarray);
                                    else if (shape == 4)
                                        gl.uniform4fv(location, bufarray);
                                }
                            }
                            else {
                                let a = command.buffer_metadata.shape[command.buffer_metadata.shape.length - 2];
                                let b = command.buffer_metadata.shape[command.buffer_metadata.shape.length - 1];
                                let bufarray = converted_buffers[command.buffer_metadata.index];
                                if (a == 2) {
                                    if (b == 2)
                                        gl.uniformMatrix2fv(location, false, bufarray);
                                    else if (b == 3)
                                        gl.uniformMatrix2x3fv(location, false, bufarray);
                                    else if (b == 4)
                                        gl.uniformMatrix2x4fv(location, false, bufarray);
                                }
                                else if (a == 3) {
                                    if (b == 2)
                                        gl.uniformMatrix3x2fv(location, false, bufarray);
                                    else if (b == 3)
                                        gl.uniformMatrix3fv(location, false, bufarray);
                                    else if (b == 4)
                                        gl.uniformMatrix3x4fv(location, false, bufarray);
                                }
                                else if (a == 4) {
                                    if (b == 2)
                                        gl.uniformMatrix4x2fv(location, false, bufarray);
                                    else if (b == 3)
                                        gl.uniformMatrix4x3fv(location, false, bufarray);
                                    else if (b == 4)
                                        gl.uniformMatrix4fv(location, false, bufarray);
                                }
                            }
                        }
                    }
                }
                break;
            case 'uniformBlockBinding':
                {
                    let res = this.get_resource(command.program);
                    const ptr = res.get('_gl_ptr');
                    const uniformblock = res.get('_info').uniforms_blocks.find((element) => { return element.name == command.uniform_block_name; });
                    if (uniformblock != undefined) {
                        gl.uniformBlockBinding(ptr, uniformblock.index, command.uniform_block_binding);
                    }
                }
                break;
            // ------------------------------- BUFFERS --------------------------------------
            case 'createBuffer':
                {
                    let res = this.get_resource(command.resource);
                    const ptr = gl.createBuffer();
                    res.set('_gl_ptr', ptr);
                    res.set('_info', { type: 'Buffer' });
                    res.save_changes();
                }
                break;
            case 'bindBuffer':
                {
                    const target = command.target;
                    if (command.buffer >= 0) {
                        const res = this.get_resource(command.buffer);
                        const ptr = res.get('_gl_ptr');
                        gl.bindBuffer(gl[target], ptr);
                        this.bound_buffers[target] = res;
                    }
                    else {
                        gl.bindBuffer(gl[target], null);
                        this.bound_buffers[target] = null;
                    }
                }
                break;
            case 'bindBufferBase':
                {
                    const target = command.target;
                    if (command.buffer >= 0) {
                        const res = this.get_resource(command.buffer);
                        const ptr = res.get('_gl_ptr');
                        gl.bindBufferBase(gl[target], command.index, ptr);
                    }
                    else {
                        gl.bindBufferBase(gl[target], command.index, null);
                    }
                }
                break;
            case 'bufferData':
                {
                    const target = command.target;
                    const usage = command.usage;
                    if (command.hasOwnProperty('buffer_metadata')) {
                        gl.bufferData(gl[target], converted_buffers[command.buffer_metadata.index], gl[usage]);
                        let buf = this.bound_buffers[target];
                        if (command.update_info && buf != null) {
                            const size = gl.getBufferParameter(gl[target], gl.BUFFER_SIZE);
                            buf.set('_info', { type: "Buffer", size: size, target: target });
                            buf.save_changes();
                        }
                    }
                    else {
                        let buf = this.bound_buffers[target];
                        gl.bufferData(gl[target], null, gl[usage]);
                        if (command.update_info && buf != null) {
                            buf.set('_info', { type: "Buffer", size: 'Undefined', target: target });
                            buf.save_changes();
                        }
                    }
                }
                break;
            case 'createUniformBuffer':
                {
                    let res = this.get_resource(command.buffer);
                    const ptr = gl.createBuffer();
                    let info = { type: 'Buffer' };
                    const prog = this.get_resource(command.program);
                    const uniformblock = prog.get('_info').uniforms_blocks.find((element) => { return element.name == command.block_name; });
                    if (uniformblock != undefined) {
                        gl.bindBuffer(gl.UNIFORM_BUFFER, ptr);
                        gl.bufferData(gl.UNIFORM_BUFFER, uniformblock.size, gl[command.usage]);
                        gl.bindBuffer(gl.UNIFORM_BUFFER, null);
                        this.bound_buffers["UNIFORM_BUFFER"] = null;
                        info["size"] = uniformblock.size;
                        info["target"] = "UNIFORM_BUFFER";
                        info["uniformblock"] = uniformblock;
                    }
                    res.set('_gl_ptr', ptr);
                    res.set('_info', info);
                    res.save_changes();
                }
                break;
            case 'bufferSubData':
            case 'bufferSubDataStr':
                {
                    const target = command.target;
                    let offset = command.dst_byte_offset;
                    if (command.cmd == 'bufferSubDataStr') {
                        offset = 0;
                        let buf = this.bound_buffers[target];
                        if (buf != null) {
                            const uniformblock = buf.get('_info').uniformblock;
                            const uniform = uniformblock.uniforms.find((element) => { return element.name == command.dst_byte_offset; });
                            if (uniform != undefined) {
                                offset = uniform.offset;
                            }
                        }
                    }
                    if (command.hasOwnProperty('buffer_metadata')) {
                        gl.bufferSubData(gl[target], offset, converted_buffers[command.buffer_metadata.index], command.src_offset);
                    }
                    else {
                        gl.bufferSubData(gl[target], offset, command.src_offset);
                    }
                }
                break;
            // ------------------------------- VERTEX ARRAYS --------------------------------------
            case 'createVertexArray':
                {
                    let res = this.get_resource(command.resource);
                    const ptr = gl.createVertexArray();
                    res.set('_gl_ptr', ptr);
                    res.set('_info', { type: 'Vertex Array Object', bindings: [] });
                    res.save_changes();
                }
                break;
            case 'bindVertexArray':
                {
                    if (command.vertex_array >= 0) {
                        const res = this.get_resource(command.vertex_array);
                        const ptr = res.get('_gl_ptr');
                        gl.bindVertexArray(ptr);
                        this.bound_vao = res;
                    }
                    else {
                        gl.bindVertexArray(null);
                        this.bound_vao = null;
                    }
                }
                break;
            case 'vertexAttribPointer':
            case 'vertexAttribIPointer':
            case 'enableVertexAttribArray':
            case 'disableVertexAttribArray':
            case 'vertexAttrib[1234]fv':
            case 'vertexAttribI4[u]iv':
            case 'vertexAttribDivisor':
                {
                    let index = -1;
                    if (typeof command.index === 'number') {
                        index = command.index;
                    }
                    else {
                        if (this.bound_program != null) {
                            const attr = this.bound_program.get('_info').attributes.find((element) => { return element.name == command.index; });
                            if (attr != undefined) {
                                index = attr.location;
                            }
                        }
                        else {
                            console.error("a program must be bound to find the attribute");
                        }
                    }
                    let buf = this.bound_buffers['ARRAY_BUFFER'];
                    if (index >= 0) {
                        index += command.index_offset;
                        if (command.cmd == "vertexAttribIPointer") {
                            gl.vertexAttribIPointer(index, command.size, gl[command.type], command.stride, command.offset);
                            if (this.bound_vao != null && buf != null) {
                                let vao_info = this.bound_vao.get('_info');
                                const buffer_uid = buf.get('uid');
                                let binding_info = vao_info.bindings.find((element) => { return element.buffer_uid == buffer_uid; });
                                if (binding_info == undefined) {
                                    binding_info = { buffer_uid: buffer_uid, attributes: [] };
                                    vao_info.bindings.push(binding_info);
                                }
                                binding_info.attributes.push({ pointer: "vertexAttribIPointer", index: index, size: command.size, type: command.type, stride: command.stride, offset: command.offset });
                                this.bound_vao.set('_info', vao_info);
                                this.bound_vao.save_changes();
                            }
                        }
                        else if (command.cmd == "vertexAttribPointer") {
                            gl.vertexAttribPointer(index, command.size, gl[command.type], command.normalized, command.stride, command.offset);
                            if (this.bound_vao != null && buf != null) {
                                let vao_info = this.bound_vao.get('_info');
                                const buffer_uid = buf.get('uid');
                                let binding_info = vao_info.bindings.find((element) => { return element.buffer_uid == buffer_uid; });
                                if (binding_info == undefined) {
                                    binding_info = { buffer_uid: buffer_uid, attributes: [] };
                                    vao_info.bindings.push(binding_info);
                                }
                                binding_info.attributes.push({ pointer: "vertexAttribPointer", index: index, size: command.size, type: command.type, normalized: command.normalized, stride: command.stride, offset: command.offset });
                                this.bound_vao.set('_info', vao_info);
                                this.bound_vao.save_changes();
                            }
                        }
                        else if (command.cmd == "enableVertexAttribArray") {
                            gl.enableVertexAttribArray(index);
                        }
                        else if (command.cmd == "disableVertexAttribArray") {
                            gl.disableVertexAttribArray(index);
                        }
                        else if (command.cmd == "vertexAttrib[1234]fv") {
                            if (command.buffer_metadata.shape[0] == 1) {
                                gl.vertexAttrib1fv(index, converted_buffers[command.buffer_metadata.index]);
                            }
                            else if (command.buffer_metadata.shape[0] == 2) {
                                gl.vertexAttrib2fv(index, converted_buffers[command.buffer_metadata.index]);
                            }
                            if (command.buffer_metadata.shape[0] == 3) {
                                gl.vertexAttrib3fv(index, converted_buffers[command.buffer_metadata.index]);
                            }
                            if (command.buffer_metadata.shape[0] == 4) {
                                gl.vertexAttrib4fv(index, converted_buffers[command.buffer_metadata.index]);
                            }
                        }
                        else if (command.cmd == "vertexAttribI4[u]iv") {
                            if (command.buffer_metadata.dtype == "uint32") {
                                gl.vertexAttribI4uiv(index, converted_buffers[command.buffer_metadata.index]);
                            }
                            else if (command.buffer_metadata.dtype == "int32") {
                                gl.vertexAttribI4iv(index, converted_buffers[command.buffer_metadata.index]);
                            }
                        }
                        else if (command.cmd == "vertexAttribDivisor") {
                            gl.vertexAttribDivisor(index, command.divisor);
                        }
                    }
                    else {
                        console.error(`attribute ${command.index} location not found`);
                    }
                }
                break;
            // ------------------------------- RENDER --------------------------------------
            case 'drawArrays':
                {
                    gl.drawArrays(gl[command.mode], command.first, command.count);
                }
                break;
            case 'drawArraysInstanced':
                {
                    gl.drawArraysInstanced(gl[command.mode], command.first, command.count, command.instance_count);
                }
                break;
            case 'drawElements':
                {
                    gl.drawElements(gl[command.mode], command.count, gl[command.type], command.offset);
                }
                break;
            case 'drawElementsInstanced':
                {
                    gl.drawElementsInstanced(gl[command.mode], command.count, gl[command.type], command.offset, command.instance_count);
                }
                break;
            // ------------------------------- FRAMEBUFFER --------------------------------------
            case 'createFramebuffer':
                {
                    let res = this.get_resource(command.resource);
                    const ptr = gl.createFramebuffer();
                    res.set('_gl_ptr', ptr);
                    res.set('_info', { type: 'Framebuffer' });
                    res.save_changes();
                }
                break;
            case 'bindFramebuffer':
                {
                    if (command.framebuffer >= 0) {
                        let res = this.get_resource(command.framebuffer);
                        gl.bindFramebuffer(gl[command.target], res.get('_gl_ptr'));
                    }
                    else {
                        gl.bindFramebuffer(gl[command.target], null);
                    }
                }
                break;
            case 'framebufferTexture2D':
                {
                    let res = this.get_resource(command.texture);
                    gl.framebufferTexture2D(gl[command.target], gl[command.attachement], gl[command.textarget], res.get('_gl_ptr'), command.level);
                }
                break;
            case 'drawBuffers':
                {
                    const buffers = command.buffers.map((element) => { return gl[element]; });
                    gl.drawBuffers(buffers);
                }
                break;
        }
    }
    register_resource(resource) {
        if (resource.get('uid') != this.resources.length) {
            console.error('uid not matching what we have internally');
        }
        this.resources.push(resource);
    }
    get_resource(index) {
        return this.resources[index];
    }
}
exports.GLModel = GLModel;
GLModel.serializers = Object.assign(Object.assign({}, base_1.DOMWidgetModel.serializers), { image_data: {
        serialize: serializeImageData,
        deserialize: deserializeImageData
    } });
class GLViewer extends base_1.DOMWidgetView {
    constructor() {
        super(...arguments);
        this.is_mouse_down = false;
        this.move_direction = [false, false, false, false];
        this.will_redraw = false;
    }
    render() {
        this.el.appendChild(this.model.canvas);
        this.resizeCanvas();
        this.model.on_some_change(['width', 'height'], this.resizeCanvas, this);
        this.el.addEventListener('mousemove', {
            handleEvent: this.onMouseMove.bind(this)
        });
        this.el.addEventListener('mousedown', {
            handleEvent: this.onMouseDown.bind(this)
        });
        this.el.addEventListener('mouseup', {
            handleEvent: this.onMouseUp.bind(this)
        });
        this.el.addEventListener('mouseout', {
            handleEvent: this.onMouseOut.bind(this)
        });
        this.el.addEventListener('keydown', {
            handleEvent: this.onKeyDown.bind(this)
        });
        this.el.addEventListener('keyup', {
            handleEvent: this.onKeyUp.bind(this)
        });
        this.el.setAttribute('tabindex', '0');
    }
    resizeCanvas() {
        this.el.setAttribute('width', this.model.get('width'));
        this.el.setAttribute('height', this.model.get('height'));
        this.model.resizeCanvas();
    }
    redraw() {
        this.will_redraw = false;
        // update movement if needed
        if (this.move_direction[0] || this.move_direction[1] || this.move_direction[2] || this.move_direction[3]) {
            let speed = this.model.get('move_speed');
            let forward_axis = matrix_1.m4getColumnK(this.model.camera_matrix);
            let side_axis = matrix_1.m4getColumnI(this.model.camera_matrix);
            let camera_pos = this.model.get('camera_pos');
            if (this.move_direction[0]) {
                camera_pos = matrix_1.vec3Add(camera_pos, matrix_1.vec3Scale(forward_axis, -speed));
            }
            if (this.move_direction[2]) {
                camera_pos = matrix_1.vec3Add(camera_pos, matrix_1.vec3Scale(forward_axis, speed));
            }
            if (this.move_direction[1]) {
                camera_pos = matrix_1.vec3Add(camera_pos, matrix_1.vec3Scale(side_axis, -speed));
            }
            if (this.move_direction[3]) {
                camera_pos = matrix_1.vec3Add(camera_pos, matrix_1.vec3Scale(side_axis, speed));
            }
            this.model.set('camera_pos', camera_pos);
            this.touch();
            // request a new frame if we are moving
            this.requestRedraw();
        }
        // re draw
        this.model.run_commands();
    }
    requestRedraw() {
        if (this.will_redraw == false) {
            this.will_redraw = true;
            requestAnimationFrame(this.redraw.bind(this));
        }
    }
    onMouseMove(event) {
        //this.model.send({ event: 'mouse_move', ...this.getCoordinates(event) }, {});
        if (this.is_mouse_down) {
            let speed = this.model.get('mouse_speed');
            this.model.set('camera_yaw', this.model.get('camera_yaw') - (event.movementX) * 0.2 * speed);
            this.model.set('camera_pitch', this.model.get('camera_pitch') - (event.movementY) * 0.2 * speed);
            this.touch();
            this.requestRedraw();
        }
    }
    onMouseDown(event) {
        this.is_mouse_down = true;
        this.model.canvas.focus();
    }
    onMouseUp(event) {
        this.is_mouse_down = false;
    }
    onMouseOut(event) {
        this.is_mouse_down = false;
        this.move_direction = [false, false, false, false];
    }
    onKeyDown(event) {
        event.preventDefault();
        event.stopPropagation();
        let keys = this.model.get('move_keys');
        if (event.repeat == false) {
            if (event.key == keys[0]) {
                this.move_direction[0] = true;
                this.requestRedraw();
            }
            else if (event.key == keys[1]) {
                this.move_direction[1] = true;
                this.requestRedraw();
            }
            else if (event.key == keys[2]) {
                this.move_direction[2] = true;
                this.requestRedraw();
            }
            else if (event.key == keys[3]) {
                this.move_direction[3] = true;
                this.requestRedraw();
            }
        }
    }
    onKeyUp(event) {
        event.preventDefault();
        event.stopPropagation();
        let keys = this.model.get('move_keys');
        if (event.key == keys[0]) {
            this.move_direction[0] = false;
        }
        else if (event.key == keys[1]) {
            this.move_direction[1] = false;
        }
        else if (event.key == keys[2]) {
            this.move_direction[2] = false;
        }
        else if (event.key == keys[3]) {
            this.move_direction[3] = false;
        }
    }
    getCoordinates(event) {
        const rect = this.el.getBoundingClientRect();
        const x = (this.model.get('width') * (event.clientX - rect.left)) / rect.width;
        const y = (this.model.get('height') * (event.clientY - rect.top)) / rect.height;
        return { x, y };
    }
}
exports.GLViewer = GLViewer;
//# sourceMappingURL=glviewer.js.map

/***/ }),

/***/ "./lib/matrix.js":
/*!***********************!*\
  !*** ./lib/matrix.js ***!
  \***********************/
/***/ ((__unused_webpack_module, exports) => {

"use strict";

Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.m4inverse = exports.m4dot = exports.m4Scale = exports.m4Zrotation = exports.m4Yrotation = exports.m4Xrotation = exports.m4Translation = exports.vec3Scale = exports.vec3Add = exports.m4getColumnK = exports.m4getColumnJ = exports.m4getColumnI = exports.m4getTranslation = exports.m4Transpose = exports.m4OrthographicProjectionMatrix = exports.m4ProjectionMatrix = void 0;
function m4ProjectionMatrix(fov_y, aspect_ratio, near, far) {
    const ymax = near * Math.tan(fov_y * Math.PI / 360.0);
    const xmax = ymax * aspect_ratio;
    return frustrum(-xmax, xmax, -ymax, ymax, near, far);
}
exports.m4ProjectionMatrix = m4ProjectionMatrix;
function frustrum(left, right, bottom, top, near, far) {
    const A = (right + left) / (right - left);
    const B = (top + bottom) / (top - bottom);
    const C = -(far + near) / (far - near);
    const D = -2. * far * near / (far - near);
    const E = 2. * near / (right - left);
    const F = 2. * near / (top - bottom);
    return [
        E, 0, A, 0,
        0, F, B, 0,
        0, 0, C, D,
        0, 0, -1, 0
    ];
}
function m4OrthographicProjectionMatrix(width, height, near, far) {
    const A = 1. / width;
    const B = 1. / height;
    const C = -(far + near) / (far - near);
    const D = -2. / (far - near);
    return [
        A, 0, 0, 0,
        0, B, 0, 0,
        0, 0, D, C,
        0, 0, 0, 1
    ];
}
exports.m4OrthographicProjectionMatrix = m4OrthographicProjectionMatrix;
function m4Transpose(m) {
    return [
        m[0], m[4], m[8], m[12],
        m[1], m[5], m[9], m[13],
        m[2], m[6], m[10], m[14],
        m[3], m[7], m[11], m[15],
    ];
}
exports.m4Transpose = m4Transpose;
function m4getTranslation(m) {
    return [
        m[3], m[7], m[11]
    ];
}
exports.m4getTranslation = m4getTranslation;
function m4getColumnI(m) {
    return [
        m[0], m[4], m[8]
    ];
}
exports.m4getColumnI = m4getColumnI;
function m4getColumnJ(m) {
    return [
        m[1], m[5], m[9]
    ];
}
exports.m4getColumnJ = m4getColumnJ;
function m4getColumnK(m) {
    return [
        m[2], m[6], m[10]
    ];
}
exports.m4getColumnK = m4getColumnK;
function vec3Add(a, b) {
    return [
        a[0] + b[0],
        a[1] + b[1],
        a[2] + b[2]
    ];
}
exports.vec3Add = vec3Add;
function vec3Scale(a, scale) {
    return [
        a[0] * scale,
        a[1] * scale,
        a[2] * scale
    ];
}
exports.vec3Scale = vec3Scale;
function m4Translation(tx, ty, tz) {
    return [
        1, 0, 0, tx,
        0, 1, 0, ty,
        0, 0, 1, tz,
        0, 0, 0, 1,
    ];
}
exports.m4Translation = m4Translation;
function m4Xrotation(angleInRadians) {
    var c = Math.cos(angleInRadians);
    var s = Math.sin(angleInRadians);
    return [
        1, 0, 0, 0,
        0, c, -s, 0,
        0, s, c, 0,
        0, 0, 0, 1,
    ];
}
exports.m4Xrotation = m4Xrotation;
function m4Yrotation(angleInRadians) {
    var c = Math.cos(angleInRadians);
    var s = Math.sin(angleInRadians);
    return [
        c, 0, s, 0,
        0, 1, 0, 0,
        -s, 0, c, 0,
        0, 0, 0, 1,
    ];
}
exports.m4Yrotation = m4Yrotation;
function m4Zrotation(angleInRadians) {
    var c = Math.cos(angleInRadians);
    var s = Math.sin(angleInRadians);
    return [
        c, -s, 0, 0,
        s, c, 0, 0,
        0, 0, 1, 0,
        0, 0, 0, 1,
    ];
}
exports.m4Zrotation = m4Zrotation;
function m4Scale(sx, sy, sz) {
    return [
        sx, 0, 0, 0,
        0, sy, 0, 0,
        0, 0, sz, 0,
        0, 0, 0, 1,
    ];
}
exports.m4Scale = m4Scale;
function m4dot(b, a) {
    return [
        b[0] * a[0] + b[1] * a[4] + b[2] * a[8] + b[3] * a[12],
        b[0] * a[1] + b[1] * a[5] + b[2] * a[9] + b[3] * a[13],
        b[0] * a[2] + b[1] * a[6] + b[2] * a[10] + b[3] * a[14],
        b[0] * a[3] + b[1] * a[7] + b[2] * a[11] + b[3] * a[15],
        b[4] * a[0] + b[5] * a[4] + b[6] * a[8] + b[7] * a[12],
        b[4] * a[1] + b[5] * a[5] + b[6] * a[9] + b[7] * a[13],
        b[4] * a[2] + b[5] * a[6] + b[6] * a[10] + b[7] * a[14],
        b[4] * a[3] + b[5] * a[7] + b[6] * a[11] + b[7] * a[15],
        b[8] * a[0] + b[9] * a[4] + b[10] * a[8] + b[11] * a[12],
        b[8] * a[1] + b[9] * a[5] + b[10] * a[9] + b[11] * a[13],
        b[8] * a[2] + b[9] * a[6] + b[10] * a[10] + b[11] * a[14],
        b[8] * a[3] + b[9] * a[7] + b[10] * a[11] + b[11] * a[15],
        b[12] * a[0] + b[13] * a[4] + b[14] * a[8] + b[15] * a[12],
        b[12] * a[1] + b[13] * a[5] + b[14] * a[9] + b[15] * a[13],
        b[12] * a[2] + b[13] * a[6] + b[14] * a[10] + b[15] * a[14],
        b[12] * a[3] + b[13] * a[7] + b[14] * a[11] + b[15] * a[15],
    ];
}
exports.m4dot = m4dot;
function m4inverse(m) {
    var tmp_0 = m[10] * m[15];
    var tmp_1 = m[14] * m[11];
    var tmp_2 = m[6] * m[15];
    var tmp_3 = m[14] * m[7];
    var tmp_4 = m[6] * m[11];
    var tmp_5 = m[10] * m[7];
    var tmp_6 = m[2] * m[15];
    var tmp_7 = m[14] * m[3];
    var tmp_8 = m[2] * m[11];
    var tmp_9 = m[10] * m[3];
    var tmp_10 = m[2] * m[7];
    var tmp_11 = m[6] * m[3];
    var tmp_12 = m[8] * m[13];
    var tmp_13 = m[12] * m[9];
    var tmp_14 = m[4] * m[13];
    var tmp_15 = m[12] * m[5];
    var tmp_16 = m[4] * m[9];
    var tmp_17 = m[8] * m[5];
    var tmp_18 = m[0] * m[13];
    var tmp_19 = m[12] * m[1];
    var tmp_20 = m[0] * m[9];
    var tmp_21 = m[8] * m[1];
    var tmp_22 = m[0] * m[5];
    var tmp_23 = m[4] * m[1];
    var t0 = (tmp_0 * m[5] + tmp_3 * m[9] + tmp_4 * m[13]) -
        (tmp_1 * m[5] + tmp_2 * m[9] + tmp_5 * m[13]);
    var t1 = (tmp_1 * m[1] + tmp_6 * m[9] + tmp_9 * m[13]) -
        (tmp_0 * m[1] + tmp_7 * m[9] + tmp_8 * m[13]);
    var t2 = (tmp_2 * m[1] + tmp_7 * m[5] + tmp_10 * m[13]) -
        (tmp_3 * m[1] + tmp_6 * m[5] + tmp_11 * m[13]);
    var t3 = (tmp_5 * m[1] + tmp_8 * m[5] + tmp_11 * m[9]) -
        (tmp_4 * m[1] + tmp_9 * m[5] + tmp_10 * m[9]);
    var d = 1.0 / (m[0] * t0 + m[4] * t1 + m[8] * t2 + m[12] * t3);
    return [
        d * t0,
        d * t1,
        d * t2,
        d * t3,
        d * ((tmp_1 * m[4] + tmp_2 * m[8] + tmp_5 * m[12]) -
            (tmp_0 * m[4] + tmp_3 * m[8] + tmp_4 * m[12])),
        d * ((tmp_0 * m[0] + tmp_7 * m[8] + tmp_8 * m[12]) -
            (tmp_1 * m[0] + tmp_6 * m[8] + tmp_9 * m[12])),
        d * ((tmp_3 * m[0] + tmp_6 * m[4] + tmp_11 * m[12]) -
            (tmp_2 * m[0] + tmp_7 * m[4] + tmp_10 * m[12])),
        d * ((tmp_4 * m[0] + tmp_9 * m[4] + tmp_10 * m[8]) -
            (tmp_5 * m[0] + tmp_8 * m[4] + tmp_11 * m[8])),
        d * ((tmp_12 * m[7] + tmp_15 * m[11] + tmp_16 * m[15]) -
            (tmp_13 * m[7] + tmp_14 * m[11] + tmp_17 * m[15])),
        d * ((tmp_13 * m[3] + tmp_18 * m[11] + tmp_21 * m[15]) -
            (tmp_12 * m[3] + tmp_19 * m[11] + tmp_20 * m[15])),
        d * ((tmp_14 * m[3] + tmp_19 * m[7] + tmp_22 * m[15]) -
            (tmp_15 * m[3] + tmp_18 * m[7] + tmp_23 * m[15])),
        d * ((tmp_17 * m[3] + tmp_20 * m[7] + tmp_23 * m[11]) -
            (tmp_16 * m[3] + tmp_21 * m[7] + tmp_22 * m[11])),
        d * ((tmp_14 * m[10] + tmp_17 * m[14] + tmp_13 * m[6]) -
            (tmp_16 * m[14] + tmp_12 * m[6] + tmp_15 * m[10])),
        d * ((tmp_20 * m[14] + tmp_12 * m[2] + tmp_19 * m[10]) -
            (tmp_18 * m[10] + tmp_21 * m[14] + tmp_13 * m[2])),
        d * ((tmp_18 * m[6] + tmp_23 * m[14] + tmp_15 * m[2]) -
            (tmp_22 * m[14] + tmp_14 * m[2] + tmp_19 * m[6])),
        d * ((tmp_22 * m[10] + tmp_16 * m[2] + tmp_21 * m[6]) -
            (tmp_20 * m[6] + tmp_23 * m[10] + tmp_17 * m[2])),
    ];
}
exports.m4inverse = m4inverse;
//# sourceMappingURL=matrix.js.map

/***/ }),

/***/ "./lib/version.js":
/*!************************!*\
  !*** ./lib/version.js ***!
  \************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";

// Copyright (c) Jerome Eippers
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.MODULE_NAME = exports.MODULE_VERSION = void 0;
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
// eslint-disable-next-line @typescript-eslint/no-var-requires
const data = __webpack_require__(/*! ../package.json */ "./package.json");
/**
 * The _model_module_version/_view_module_version this package implements.
 *
 * The html widget manager assumes that this is the same as the npm package
 * version number.
 */
exports.MODULE_VERSION = data.version;
/*
 * The current package name.
 */
exports.MODULE_NAME = data.name;
//# sourceMappingURL=version.js.map

/***/ }),

/***/ "./lib/widgets.js":
/*!************************!*\
  !*** ./lib/widgets.js ***!
  \************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __exportStar = (this && this.__exportStar) || function(m, exports) {
    for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports, p)) __createBinding(exports, m, p);
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
__exportStar(__webpack_require__(/*! ./glviewer */ "./lib/glviewer.js"), exports);
__exportStar(__webpack_require__(/*! ./glresource */ "./lib/glresource.js"), exports);
//# sourceMappingURL=widgets.js.map

/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./css/widget.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./css/widget.css ***!
  \**************************************************************/
/***/ ((module, exports, __webpack_require__) => {

// Imports
var ___CSS_LOADER_API_IMPORT___ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
exports = ___CSS_LOADER_API_IMPORT___(false);
// Module
exports.push([module.id, ".ipywebgl-json-display {\r\n  padding: 10px;\r\n  font-family: sans-serif;\r\n  background-color: #f2f2f2;\r\n  margin-left: 20px;\r\n}\r\n\r\n.ipywebgl-json-key {\r\n  font-weight: bold;\r\n  color: #333;\r\n}\r\n\r\n.ipywebgl-json-value {\r\n  color: #555;\r\n}", ""]);
// Exports
module.exports = exports;


/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/api.js":
/*!*****************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/api.js ***!
  \*****************************************************/
/***/ ((module) => {

"use strict";


/*
  MIT License http://www.opensource.org/licenses/mit-license.php
  Author Tobias Koppers @sokra
*/
// css base code, injected by the css-loader
// eslint-disable-next-line func-names
module.exports = function (useSourceMap) {
  var list = []; // return the list of modules as css string

  list.toString = function toString() {
    return this.map(function (item) {
      var content = cssWithMappingToString(item, useSourceMap);

      if (item[2]) {
        return "@media ".concat(item[2], " {").concat(content, "}");
      }

      return content;
    }).join('');
  }; // import a list of modules into the list
  // eslint-disable-next-line func-names


  list.i = function (modules, mediaQuery, dedupe) {
    if (typeof modules === 'string') {
      // eslint-disable-next-line no-param-reassign
      modules = [[null, modules, '']];
    }

    var alreadyImportedModules = {};

    if (dedupe) {
      for (var i = 0; i < this.length; i++) {
        // eslint-disable-next-line prefer-destructuring
        var id = this[i][0];

        if (id != null) {
          alreadyImportedModules[id] = true;
        }
      }
    }

    for (var _i = 0; _i < modules.length; _i++) {
      var item = [].concat(modules[_i]);

      if (dedupe && alreadyImportedModules[item[0]]) {
        // eslint-disable-next-line no-continue
        continue;
      }

      if (mediaQuery) {
        if (!item[2]) {
          item[2] = mediaQuery;
        } else {
          item[2] = "".concat(mediaQuery, " and ").concat(item[2]);
        }
      }

      list.push(item);
    }
  };

  return list;
};

function cssWithMappingToString(item, useSourceMap) {
  var content = item[1] || ''; // eslint-disable-next-line prefer-destructuring

  var cssMapping = item[3];

  if (!cssMapping) {
    return content;
  }

  if (useSourceMap && typeof btoa === 'function') {
    var sourceMapping = toComment(cssMapping);
    var sourceURLs = cssMapping.sources.map(function (source) {
      return "/*# sourceURL=".concat(cssMapping.sourceRoot || '').concat(source, " */");
    });
    return [content].concat(sourceURLs).concat([sourceMapping]).join('\n');
  }

  return [content].join('\n');
} // Adapted from convert-source-map (MIT)


function toComment(sourceMap) {
  // eslint-disable-next-line no-undef
  var base64 = btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap))));
  var data = "sourceMappingURL=data:application/json;charset=utf-8;base64,".concat(base64);
  return "/*# ".concat(data, " */");
}

/***/ }),

/***/ "./css/widget.css":
/*!************************!*\
  !*** ./css/widget.css ***!
  \************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

var api = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
            var content = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./widget.css */ "./node_modules/css-loader/dist/cjs.js!./css/widget.css");

            content = content.__esModule ? content.default : content;

            if (typeof content === 'string') {
              content = [[module.id, content, '']];
            }

var options = {};

options.insert = "head";
options.singleton = false;

var update = api(content, options);



module.exports = content.locals || {};

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js":
/*!****************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js ***!
  \****************************************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

"use strict";


var isOldIE = function isOldIE() {
  var memo;
  return function memorize() {
    if (typeof memo === 'undefined') {
      // Test for IE <= 9 as proposed by Browserhacks
      // @see http://browserhacks.com/#hack-e71d8692f65334173fee715c222cb805
      // Tests for existence of standard globals is to allow style-loader
      // to operate correctly into non-standard environments
      // @see https://github.com/webpack-contrib/style-loader/issues/177
      memo = Boolean(window && document && document.all && !window.atob);
    }

    return memo;
  };
}();

var getTarget = function getTarget() {
  var memo = {};
  return function memorize(target) {
    if (typeof memo[target] === 'undefined') {
      var styleTarget = document.querySelector(target); // Special case to return head of iframe instead of iframe itself

      if (window.HTMLIFrameElement && styleTarget instanceof window.HTMLIFrameElement) {
        try {
          // This will throw an exception if access to iframe is blocked
          // due to cross-origin restrictions
          styleTarget = styleTarget.contentDocument.head;
        } catch (e) {
          // istanbul ignore next
          styleTarget = null;
        }
      }

      memo[target] = styleTarget;
    }

    return memo[target];
  };
}();

var stylesInDom = [];

function getIndexByIdentifier(identifier) {
  var result = -1;

  for (var i = 0; i < stylesInDom.length; i++) {
    if (stylesInDom[i].identifier === identifier) {
      result = i;
      break;
    }
  }

  return result;
}

function modulesToDom(list, options) {
  var idCountMap = {};
  var identifiers = [];

  for (var i = 0; i < list.length; i++) {
    var item = list[i];
    var id = options.base ? item[0] + options.base : item[0];
    var count = idCountMap[id] || 0;
    var identifier = "".concat(id, " ").concat(count);
    idCountMap[id] = count + 1;
    var index = getIndexByIdentifier(identifier);
    var obj = {
      css: item[1],
      media: item[2],
      sourceMap: item[3]
    };

    if (index !== -1) {
      stylesInDom[index].references++;
      stylesInDom[index].updater(obj);
    } else {
      stylesInDom.push({
        identifier: identifier,
        updater: addStyle(obj, options),
        references: 1
      });
    }

    identifiers.push(identifier);
  }

  return identifiers;
}

function insertStyleElement(options) {
  var style = document.createElement('style');
  var attributes = options.attributes || {};

  if (typeof attributes.nonce === 'undefined') {
    var nonce =  true ? __webpack_require__.nc : 0;

    if (nonce) {
      attributes.nonce = nonce;
    }
  }

  Object.keys(attributes).forEach(function (key) {
    style.setAttribute(key, attributes[key]);
  });

  if (typeof options.insert === 'function') {
    options.insert(style);
  } else {
    var target = getTarget(options.insert || 'head');

    if (!target) {
      throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");
    }

    target.appendChild(style);
  }

  return style;
}

function removeStyleElement(style) {
  // istanbul ignore if
  if (style.parentNode === null) {
    return false;
  }

  style.parentNode.removeChild(style);
}
/* istanbul ignore next  */


var replaceText = function replaceText() {
  var textStore = [];
  return function replace(index, replacement) {
    textStore[index] = replacement;
    return textStore.filter(Boolean).join('\n');
  };
}();

function applyToSingletonTag(style, index, remove, obj) {
  var css = remove ? '' : obj.media ? "@media ".concat(obj.media, " {").concat(obj.css, "}") : obj.css; // For old IE

  /* istanbul ignore if  */

  if (style.styleSheet) {
    style.styleSheet.cssText = replaceText(index, css);
  } else {
    var cssNode = document.createTextNode(css);
    var childNodes = style.childNodes;

    if (childNodes[index]) {
      style.removeChild(childNodes[index]);
    }

    if (childNodes.length) {
      style.insertBefore(cssNode, childNodes[index]);
    } else {
      style.appendChild(cssNode);
    }
  }
}

function applyToTag(style, options, obj) {
  var css = obj.css;
  var media = obj.media;
  var sourceMap = obj.sourceMap;

  if (media) {
    style.setAttribute('media', media);
  } else {
    style.removeAttribute('media');
  }

  if (sourceMap && typeof btoa !== 'undefined') {
    css += "\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap)))), " */");
  } // For old IE

  /* istanbul ignore if  */


  if (style.styleSheet) {
    style.styleSheet.cssText = css;
  } else {
    while (style.firstChild) {
      style.removeChild(style.firstChild);
    }

    style.appendChild(document.createTextNode(css));
  }
}

var singleton = null;
var singletonCounter = 0;

function addStyle(obj, options) {
  var style;
  var update;
  var remove;

  if (options.singleton) {
    var styleIndex = singletonCounter++;
    style = singleton || (singleton = insertStyleElement(options));
    update = applyToSingletonTag.bind(null, style, styleIndex, false);
    remove = applyToSingletonTag.bind(null, style, styleIndex, true);
  } else {
    style = insertStyleElement(options);
    update = applyToTag.bind(null, style, options);

    remove = function remove() {
      removeStyleElement(style);
    };
  }

  update(obj);
  return function updateStyle(newObj) {
    if (newObj) {
      if (newObj.css === obj.css && newObj.media === obj.media && newObj.sourceMap === obj.sourceMap) {
        return;
      }

      update(obj = newObj);
    } else {
      remove();
    }
  };
}

module.exports = function (list, options) {
  options = options || {}; // Force single-tag solution on IE6-9, which has a hard limit on the # of <style>
  // tags it will allow on a page

  if (!options.singleton && typeof options.singleton !== 'boolean') {
    options.singleton = isOldIE();
  }

  list = list || [];
  var lastIdentifiers = modulesToDom(list, options);
  return function update(newList) {
    newList = newList || [];

    if (Object.prototype.toString.call(newList) !== '[object Array]') {
      return;
    }

    for (var i = 0; i < lastIdentifiers.length; i++) {
      var identifier = lastIdentifiers[i];
      var index = getIndexByIdentifier(identifier);
      stylesInDom[index].references--;
    }

    var newLastIdentifiers = modulesToDom(newList, options);

    for (var _i = 0; _i < lastIdentifiers.length; _i++) {
      var _identifier = lastIdentifiers[_i];

      var _index = getIndexByIdentifier(_identifier);

      if (stylesInDom[_index].references === 0) {
        stylesInDom[_index].updater();

        stylesInDom.splice(_index, 1);
      }
    }

    lastIdentifiers = newLastIdentifiers;
  };
};

/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

"use strict";
module.exports = JSON.parse('{"name":"ipywebgl","version":"0.3.0","description":"A Custom Jupyter Widget Library","keywords":["jupyter","jupyterlab","jupyterlab-extension","widgets"],"files":["lib/**/*.js","dist/*.js","css/*.css"],"homepage":"https://github.com/JeromeEippers/ipywebgl","bugs":{"url":"https://github.com/JeromeEippers/ipywebgl/issues"},"license":"BSD-3-Clause","author":{"name":"Jerome Eippers","email":"jerome@eippers.be"},"main":"lib/index.js","types":"./lib/index.d.ts","repository":{"type":"git","url":"https://github.com/JeromeEippers/ipywebgl"},"scripts":{"build":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension:dev","build:prod":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","build:nbextension":"webpack","clean":"yarn run clean:lib && yarn run clean:nbextension && yarn run clean:labextension","clean:lib":"rimraf lib","clean:labextension":"rimraf ipywebgl/labextension","clean:nbextension":"rimraf ipywebgl/nbextension/static/index.js","lint":"eslint . --ext .ts,.tsx --fix","lint:check":"eslint . --ext .ts,.tsx","prepack":"yarn run build:lib","watch":"npm-run-all -p watch:*","watch:lib":"tsc -w","watch:nbextension":"webpack --watch --mode=development","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@jupyter-widgets/base":"^1.1.10 || ^2 || ^3 || ^4 || ^5 || ^6"},"devDependencies":{"@babel/core":"^7.5.0","@babel/preset-env":"^7.5.0","@jupyter-widgets/base-manager":"^1.0.2","@jupyterlab/builder":"^3.0.0","@lumino/application":"^1.6.0","@lumino/widgets":"^1.6.0","@types/jest":"^26.0.0","@types/webpack-env":"^1.13.6","@typescript-eslint/eslint-plugin":"^3.6.0","@typescript-eslint/parser":"^3.6.0","acorn":"^7.2.0","css-loader":"^3.2.0","eslint":"^7.4.0","eslint-config-prettier":"^6.11.0","eslint-plugin-prettier":"^3.1.4","fs-extra":"^7.0.0","identity-obj-proxy":"^3.0.0","jest":"^26.0.0","mkdirp":"^0.5.1","npm-run-all":"^4.1.3","prettier":"^2.0.5","rimraf":"^2.6.2","source-map-loader":"^1.1.3","style-loader":"^1.0.0","ts-jest":"^26.0.0","ts-loader":"^8.0.0","typescript":"~4.1.3","webpack":"^5.61.0","webpack-cli":"^4.0.0"},"jupyterlab":{"extension":"lib/plugin","outputDir":"ipywebgl/labextension/","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}}}}');

/***/ })

}]);
//# sourceMappingURL=lib_widgets_js.faf7d4be5b9d6f575f9f.js.map