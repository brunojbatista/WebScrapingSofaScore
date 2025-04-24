"""
    Destinado a colocar os código no formato javascript:
"""

###############################################################################################################################
###############################################################################################################################
###############################################################################################################################


STRING = r"""

function clear_accents(name) {
    return name.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
}

function sub_latin_caracters(content, repl) {
    return content.replace(/[\u00A1-\u00FF]/g, repl);
}

// Cria um regex baseado na string de entrada
function create_regex_latin_str(name) {
    // Escapa caracteres especiais
    let nameFormatted = name.replace(/['()\[\]_+\-\/\\.,;?!$&*=%]/g, '\\$&');
    
    // Substitui palavras comuns por espaço e substitui caracteres latinos
    nameFormatted = sub_latin_caracters(
        nameFormatted.replace(/\b(do|da|de|dos|das|ou|e|a|o|i|u|&|as|os|no|na|nos|nas)\b/gi, ' '),
        '.'
    );

    // Remove espaços extras e converte para regex
    const regex = `^\\s*${nameFormatted.replace(/\s+/g, '.+?')}\\s*$`;
    return regex;
}

"""

###############################################################################################################################
###############################################################################################################################
###############################################################################################################################

AUTOMATION = r"""

function sleep(milliseconds) {
    return new Promise(resolve => {
        setTimeout(resolve, milliseconds);
    });
}

// Verificar se um variavel é do tipo elemento da DOM
function isElement(element) {
    return element instanceof Element || element instanceof HTMLDocument;  
}

// Função que executa uma função assincrona até que ela retorne true ou até o timeout definido
function running(asyncFunction, timeout, interval = 50) {
    return new Promise((resolve, reject) => {
        const startTime = Date.now();
        let hasFirstCycle = false

        async function execute() {
            try {
                // Verifica se o tempo limite foi atingido
                if (Date.now() - startTime > timeout && hasFirstCycle) {
                    return resolve(false);
                }

                // Executa a função fornecida
                const result = await asyncFunction();

                // Se a função retornar true, resolve a Promise
                if (result === true) {
                    return resolve(true);
                }

                hasFirstCycle = true

                // Caso contrário, espera o intervalo definido antes de tentar novamente
                setTimeout(execute, interval);
            } catch (error) {
                // Rejeita a Promise em caso de erro na função fornecida
                return reject(error);
            }
        }

        // Inicia o loop
        execute();
    });
}

// Irá buscar o elemento até o timeout definido
function getElement(xpath, ref = document, timeout = 60000) {
    return new Promise(
        (resolve, reject) => {
            running(
                async () => {
                    const element = document.evaluate(xpath, ref, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    return element !== null
                },
                timeout
            )
            .then(
                async (status) => {
                    if (status) {
                        const element = document.evaluate(xpath, ref, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                        resolve(element)
                    } else {
                        resolve(null)
                    }
                }
            )
            .catch(e => reject(e))
        }
    )
}

// Irá buscar os elementos até o timeout definido
function getElements(xpath, ref = document, timeout = 60000) {
    return new Promise(
        (resolve, reject) => {
            running(
                async () => {
                    const snapshot  = document.evaluate(xpath, ref, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
                    return snapshot.snapshotLength >= 0
                },
                timeout
            )
            .then(
                async (status) => {
                    if (status) {
                        const snapshot  = document.evaluate(xpath, ref, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
                        let elements = []
                        for (let i = 0; i < snapshot.snapshotLength; i++) {
                            elements.push(snapshot.snapshotItem(i));
                        }
                        resolve(elements)
                    } else {
                        resolve([])
                    }
                }
            )
            .catch(e => reject(e))
        }
    )
}

// Irá verificar se existe o elemento até o timeout definido
function hasElement(xpath, ref = document, timeout = 60000) {
    return new Promise(
        (resolve, reject) => {
            getElement(xpath, ref, timeout)
            .then(
                (element) => {
                    if (element) {
                        resolve(true)
                    } else {
                        resolve(false)
                    }
                }
            )
            .catch(e => reject(e))
        }
    )
}

// Irá verificar se não existe o elemento até o timeout definido
function hasNoElement(xpath, ref = document, timeout = 60000) {
    return new Promise(
        (resolve, reject) => {
            running(
                async () => {
                    const element = document.evaluate(xpath, ref, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    return element === null
                },
                timeout
            )
            .then(
                (status) => {
                    if (status) {
                        resolve(true)
                    } else {
                        resolve(false)
                    }
                }
            )
            .catch(e => reject(e))
        }
    )
}

// Irá verificar se existe os elementos até o timeout definido
function hasElements(xpath, ref = document, timeout = 60000) {
    return new Promise(
        (resolve, reject) => {
            getElements(xpath, ref, timeout)
            .then(
                (elements) => {
                    if (elements.length > 0) {
                        resolve(true)
                    } else {
                        resolve(false)
                    }
                }
            )
            .catch(e => reject(e))
        }
    )
}

// Irá verificar se não existe os elementos até o timeout definido
function hasNoElements(xpath, ref = document, timeout = 60000) {
    return new Promise(
        (resolve, reject) => {
            running(
                async () => {
                    const snapshot  = document.evaluate(xpath, ref, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
                    return snapshot.snapshotLength <= 0
                },
                timeout
            )
            .then(
                async (status) => {
                    if (status) {
                        const snapshot  = document.evaluate(xpath, ref, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
                        if (snapshot.snapshotLength <= 0) {
                            resolve(true)
                        } else {
                            resolve(false)
                        }
                    } else {
                        resolve(false)
                    }
                }
            )
            .catch(e => reject(e))
        }
    )
}

// Irá retornar o texto até o timeout definido
function getText(xpath_or_element, ref = document, timeout = 60000) {
    return new Promise(
        (resolve, reject) => {
			if (isElement(xpath_or_element)) {
				let element = xpath_or_element
				let text = element.textContent.trim()
				resolve(text)
			} else {
				getElement(xpath_or_element, ref, timeout)
				.then(
					(element) => {
						if (element) {
							let text = element.textContent.trim()
							resolve(text)
						} else {
							resolve(null)
						}
					}
				)
				.catch(e => reject(e))
			}
        }
    );
}

// Irá retornar o valor de attr_name até o timeout definido
function getAttr(xpath_or_element, attr_name, ref = document, timeout = 60000) {
    return new Promise(
        (resolve, reject) => {
			if (isElement(xpath_or_element)) {
				let element = xpath_or_element
				if (element.hasAttribute(attr_name)) {
					let attrValue = element.getAttribute(attr_name)
					resolve(attrValue)
				} else {
					resolve(null)
				}
			} else {
				getElement(xpath_or_element, ref, timeout)
				.then(
					(element) => {
						if (element) {
							if (element.hasAttribute(attr_name)) {
								let attrValue = element.getAttribute(attr_name)
								resolve(attrValue)
							} else {
								resolve(null)
							}
						} else {
							resolve(null)
						}
					}
				)
				.catch(e => reject(e))
			}
        }
    );
}

// Irá esperar o attr_name aparecer até o timeout definido
function hasAttr(xpath_or_element, attr_name, ref = document, timeout = 60000) {
    return new Promise(
        (resolve, reject) => {
			if (isElement(xpath_or_element)) {
				let element = xpath_or_element
				if (element.hasAttribute(attr_name)) {
					resolve(true)
				} else {
					resolve(false)
				}
			} else {
				getElement(xpath_or_element, ref, timeout)
				.then(
					(element) => {
						if (element) {
							if (element.hasAttribute(attr_name)) {
								resolve(true)
							} else {
								resolve(false)
							}
						} else {
							resolve(false)
						}
					}
				)
				.catch(e => reject(e))
			}
        }
    );
}

// Irá esperar o attr_name ficar com o valor de attr_value até o timeout definido
function hasAttrValue(xpath_or_element, attr_name, attr_value, ref = document, timeout = 60000) {
    return new Promise(
        (resolve, reject) => {
			if (isElement(xpath_or_element)) {
				let element = xpath_or_element
				if (!element.hasAttribute(attr_name)) return resolve(false)
				let attrValue = element.getAttribute(attr_name)
				return resolve(attrValue === attr_value)
			} else {
				running(
					() => {
						const element = document.evaluate(xpath_or_element, ref, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
						if (!element) return false
						if (!element.hasAttribute(attr_name)) return false
						let attrValue = element.getAttribute(attr_name)
						return attrValue === attr_value
					},
					timeout
				)
				.then(
					async (status) => {
						if (status) {
							const element = document.evaluate(xpath_or_element, ref, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
							if (!element.hasAttribute(attr_name)) return resolve(false)
							let attrValue = element.getAttribute(attr_name)
							return resolve(attrValue === attr_value)
						} else {
							resolve(false)
						}
					}
				)
				.catch(e => reject(e))
			}
        }
    );
}

// Irá retornar o valor do estilo até o timeout definido
function getStyle(xpath_or_element, style_name, ref = document, timeout = 60000) {
    return new Promise(
        (resolve, reject) => {
			if (isElement(xpath_or_element)) {
				let element = xpath_or_element
                let style = window.getComputedStyle(element);
                if (style.getPropertyValue(style_name)) {
                    let value = style.getPropertyValue(style_name);
                    resolve(value)
                } else {
                    resolve(null)
                }
			} else {
				getElement(xpath_or_element, ref, timeout)
				.then(
					(element) => {
						if (element) {
                            let style = window.getComputedStyle(element);
                            if (style.getPropertyValue(style_name)) {
                                let value = style.getPropertyValue(style_name);
                                resolve(value)
                            } else {
                                resolve(null)
                            }
						} else {
							resolve(null)
						}
					}
				)
				.catch(e => reject(e))
			}
        }
    );
}

// Irá retorna true quando o valor do estilo mudar ou até o timeout definido
function waitChangeStyle(xpath_or_element, style_name, fn, ref = document, timeout = 60000) {
    return new Promise(
        async (resolve, reject) => {
            var value_before = await getStyle(xpath_or_element, style_name, ref, 0)
            await fn()
            running(
                async () => {
                    var value_current = await getStyle(xpath_or_element, style_name, ref, 0)
                    console.log('value_before', value_before)
                    console.log('value_current', value_current)
                    return value_current != value_before
                },
                timeout
            )
            .then(
                async (status) => {
                    resolve(status)
                }
            )
            .catch(e => reject(e))
        }
    );
}

// Irá clicar no elemento até o timeout definido
function clickElement(xpath_or_element, ref = document, timeout = 60000) {
    return new Promise(
        (resolve, reject) => {
			if (isElement(xpath_or_element)) {
				let element = xpath_or_element
				element.click()
				resolve(true)
			} else {
				getElement(xpath_or_element, ref, timeout)
				.then(
					(element) => {
						if (element) {
							element.click()
							resolve(true)
						} else {
							resolve(false)
						}
					}
				)
				.catch(e => reject(e))
			}
        }
    );
}

// Irá mover o mouse em cima do elemento no timeout definido
function mouseMove(xpath_or_element, ref = document, timeout = 60000) {
    return new Promise(
        (resolve, reject) => {
			if (isElement(xpath_or_element)) {
				let element = xpath_or_element
				let rect = element.getBoundingClientRect();
				let evt = new MouseEvent('mousemove', {
					bubbles: true,
					cancelable: true,
					clientX: rect.left + (rect.width / 2),
					clientY: rect.top + (rect.height / 2)
				});
				element.dispatchEvent(evt);
				resolve(true)
			} else {
				getElement(xpath_or_element, ref, timeout)
				.then(
					(element) => {
						if (element) {
							let rect = element.getBoundingClientRect();
							let evt = new MouseEvent('mousemove', {
								bubbles: true,
								cancelable: true,
								clientX: rect.left + (rect.width / 2),
								clientY: rect.top + (rect.height / 2)
							});
							element.dispatchEvent(evt);
							resolve(true)
						} else {
							resolve(false)
						}
					}
				)
				.catch(e => reject(e))
			}
        }
    );
}

// Irá mover o mouse em cima do elemento no timeout definido
function simulateMouseOver(xpath_or_element, ref = document, timeout = 60000) {
    return new Promise(
        (resolve, reject) => {
			if (isElement(xpath_or_element)) {
				let element = xpath_or_element
				// Dispatch mouseover
				element.dispatchEvent(new MouseEvent("mouseover", { bubbles: true, cancelable: true, view: window }));
				// Dispatch mouseenter
				element.dispatchEvent(new MouseEvent("mouseenter", { bubbles: true, cancelable: true, view: window }));
				// Dispatch mousemove
				const rect = element.getBoundingClientRect();
				const centerX = rect.left + rect.width / 2;
				const centerY = rect.top + rect.height / 2;

				element.dispatchEvent(new MouseEvent("mousemove", {
					bubbles: true,
					cancelable: true,
					view: window,
					clientX: centerX,
					clientY: centerY
				}));
				resolve(true)
			} else {
				getElement(xpath_or_element, ref, timeout)
				.then(
					(element) => {
						if (element) {
							// Dispatch mouseover
							element.dispatchEvent(new MouseEvent("mouseover", { bubbles: true, cancelable: true, view: window }));
							// Dispatch mouseenter
							element.dispatchEvent(new MouseEvent("mouseenter", { bubbles: true, cancelable: true, view: window }));
							// Dispatch mousemove
							const rect = element.getBoundingClientRect();
							const centerX = rect.left + rect.width / 2;
							const centerY = rect.top + rect.height / 2;

							element.dispatchEvent(new MouseEvent("mousemove", {
								bubbles: true,
								cancelable: true,
								view: window,
								clientX: centerX,
								clientY: centerY
							}));
							resolve(true)
						} else {
							resolve(false)
						}
					}
				)
				.catch(e => reject(e))
			}
        }
    );
}

// Irá executar o pressionamento de alguma tecla no elemento até o timeout definido
function pressKeyElement(xpath_or_element, key_name, ref = document, timeout = 60000) {
	function simulateKeyDownByName(element, keyName) {
		// Mapeamento de teclas para seus respectivos keyCodes
		const keyMap = {
			"Backspace": 8,
			"Tab": 9,
			"Enter": 13,
			"Shift": 16,
			"Control": 17,
			"Alt": 18,
			"Pause": 19,
			"CapsLock": 20,
			"Escape": 27,
			"Space": 32,
			"ArrowLeft": 37,
			"ArrowUp": 38,
			"ArrowRight": 39,
			"ArrowDown": 40,
			"Delete": 46
		};

		// Se for uma tecla especial, pega o keyCode do mapeamento
		const keyCode = keyMap[keyName] || keyName.charCodeAt(0);

		// Criar o evento de teclado
		const event = new KeyboardEvent("keydown", {
			key: keyName,
			code: `Key${keyName.toUpperCase()}`,
			keyCode: keyCode,
			which: keyCode,
			bubbles: true
		});

		// Disparar o evento no elemento
		element.dispatchEvent(event);
	}
    return new Promise(
        async (resolve, reject) => {
			if (isElement(xpath_or_element)) {
				let element = xpath_or_element
                await new Promise((resolve) => setTimeout(resolve, 100)); // Aguarda um pequeno tempo
				simulateKeyDownByName(element, key_name)
				resolve(true)
			} else {
				getElement(xpath_or_element, ref, timeout)
				.then(
					async (element) => {
						if (element) {
                            await new Promise((resolve) => setTimeout(resolve, 100)); // Aguarda um pequeno tempo
							simulateKeyDownByName(element, key_name)
							resolve(true)
						} else {
							resolve(false)
						}
					}
				)
				.catch(e => reject(e))
			}
        }
    );
}

function pressEnterElement(xpath_or_element, ref = document, timeout = 60000) {
	return pressKeyElement(xpath_or_element, 'Enter')
}

// Irá executar a escrita de dado no elemento até o timeout definido
function writeInputElement(xpath_or_element, text, ref = document, timeout = 60000) {
	function write(element, text) {
		element.value = text; // Define o valor diretamente
		element.dispatchEvent(new Event('input', { bubbles: true })); // Dispara evento 'input'
		element.dispatchEvent(new Event('change', { bubbles: true })); // Dispara evento 'change'
	}

	return new Promise((resolve, reject) => {
		if (isElement(xpath_or_element)) {
			write(xpath_or_element, text);
			resolve(true);
		} else {
			getElement(xpath_or_element, ref, timeout)
				.then((element) => {
					if (element) {
						write(element, text);
						resolve(true);
					} else {
						resolve(false);
					}
				})
				.catch((e) => reject(e));
		}
	});
}


// Irá executar a limpeza de dado no elemento até o timeout definido
function clearInputElement(xpath_or_element, text, ref = document, timeout = 60000) {
	return writeInputElement(xpath_or_element, "", ref, timeout)
}

// Irá detectar a mudanda do elemento após a execução do callback até o timeout definido
function detectChangeElementAfterCallback(xpath_or_element, callback, ref = document, timeout = 60000) {
    function detect(element) {
        return new Promise((resolve, reject) => {
			let timeout_ref = null
			
            let initialState = {
                value: element.value, // Armazena o valor inicial para inputs
                innerText: element.innerText, // Armazena o conteúdo de texto
                outerHTML: element.outerHTML, // Armazena o HTML externo completo
                attributes: getAttributes(element) // Armazena os atributos do elemento
            };

            const observer = new MutationObserver(() => {
                const currentState = {
                    value: element.value,
                    innerText: element.innerText,
                    outerHTML: element.outerHTML,
                    attributes: getAttributes(element)
                };

                if (hasChanged(initialState, currentState)) {
                    clearTimeout(timeout_ref); // Cancela o timeout
                    observer.disconnect(); // Para de observar
                    resolve(true); // Retorna que houve mudança
                }
            });

            observer.observe(element, { attributes: true, childList: true, subtree: true, characterData: true });

            // Adiciona listener de evento 'input' para capturar mudança de 'value'
            const inputListener = () => {
                if (element.value !== initialState.value) {
                    clearTimeout(timeout_ref);
                    element.removeEventListener("input", inputListener);
                    observer.disconnect();
                    resolve(true);
                }
            };
            element.addEventListener("input", inputListener);

            // Executa o callback para disparar a mudança no elemento
            Promise.resolve(callback()).then(() => {
                // Timeout para evitar espera infinita
					timeout_ref = setTimeout(() => {
                    element.removeEventListener("input", inputListener);
                    observer.disconnect();
                    resolve(false); // Retorna falso se não houver mudança dentro do tempo
                }, timeout);
            });
        });
    }

    // Função para comparar o estado anterior e atual
    function hasChanged(initialState, currentState) {
        return (
            initialState.value !== currentState.value ||
            initialState.innerText !== currentState.innerText ||
            initialState.outerHTML !== currentState.outerHTML ||
            !areAttributesEqual(initialState.attributes, currentState.attributes)
        );
    }

    // Função para comparar atributos
    function areAttributesEqual(attrs1, attrs2) {
        if (Object.keys(attrs1).length !== Object.keys(attrs2).length) return false;
        for (let key in attrs1) {
            if (attrs1[key] !== attrs2[key]) return false;
        }
        return true;
    }

    // Função para obter todos os atributos de um elemento
    function getAttributes(element) {
        let attributes = {};
        for (let i = 0; i < element.attributes.length; i++) {
            let attr = element.attributes[i];
            attributes[attr.name] = attr.value;
        }
        return attributes;
    }

    return new Promise(async (resolve, reject) => {
        let status_detect = false
        if (isElement(xpath_or_element)) {
            let element = xpath_or_element;
            status_detect = await detect(element);
            resolve(status_detect);
        } else {
            getElement(xpath_or_element, ref, timeout)
                .then(async (element) => {
                    if (element) {
                        status_detect = await detect(element);
                        resolve(status_detect);
                    } else {
                        resolve(false);
                    }
                })
                .catch((e) => reject(e));
        }
    });
}

// Irá detectar a mudanda do elemento até o timeout definido
function detectChangeElement(xpath_or_element, ref = document, timeout = 60000) {
	return detectChangeElementAfterCallback(xpath_or_element, () => {}, ref, timeout)
}

"""

###############################################################################################################################
###############################################################################################################################
###############################################################################################################################

JAVASCRIPT_CODE = STRING + AUTOMATION