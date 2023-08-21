const getState = ({getStore, getActions, setStore}) => {
	return {
		store: {
			message: null,
			demo: [
				{
					title: "FIRST",
					background: "white",
					initial: "white"
				},
				{
					title: "SECOND",
					background: "white",
					initial: "white"
				}
			]
		},
		actions: {
			// Use getActions to call a function within a fuction
			exampleFunction: () => {
				getActions().changeColor(0, "green");
			},
			getMessage: async () => {
				try {
					// Fetching data from the backend
					const response = await fetch(process.env.BACKEND_URL + "/api/hello")
                    if (response.ok) {
                        const data = await response.json()
                        setStore({message: data.message})
                        // Don't forget to return something, that is how the async resolves
                        return data;
                    } else {
                        console.log(response.status, response.statusText)
                    }
				} catch(error) {
					console.log("Error loading message from backend", error)
				}
			},
			changeColor: (index, color) => {
				// Get the store
				const store = getStore();
				// We have to loop the entire demo array to look for the respective index and change its color
				const demo = store.demo.map((item, i) => {
					if (i === index) {
                        item.background = color;
                    }
					return item;
				});
				// Reset the global store
				setStore({demo: demo});
			}
		}
	};
};


export default getState;
